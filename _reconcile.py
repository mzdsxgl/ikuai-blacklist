import subprocess, re
from collections import Counter

def reg_domain(host):
    host = host.lower().strip().rstrip('.')
    parts = host.split('.')
    if len(parts) < 2:
        return host
    last2 = parts[-2] + '.' + parts[-1]
    if last2 in {'com.cn','net.cn','org.cn','gov.cn','edu.cn','co.uk','com.hk','com.tw','com.au'}:
        return '.'.join(parts[-3:]) if len(parts) >= 3 else host
    return '.'.join(parts[-2:])

def load(ref):
    txt = subprocess.check_output(['git','show',ref+':ikuai_blacklist_hosts.txt']).decode('utf-8')
    return [l.split('0.0.0.0',1)[1].strip() for l in txt.splitlines() if l.startswith('0.0.0.0 ')]

orig = load('HEAD~1')   # 1456
cur  = load('HEAD')     # 1281
so, sc = set(orig), set(cur)

unchanged = so & sc                       # 两边都有
in_orig_not_cur = so - sc                # 原版有、现版无

# 其中: 根域在现版 -> 被"合并"进根域 (不是真删)
merged = [(d, reg_domain(d)) for d in in_orig_not_cur if reg_domain(d) in sc]
# 其中: 根域也不在现版 -> 真删除(脏数据)
truly_deleted = sorted(d for d in in_orig_not_cur if reg_domain(d) not in sc)
new_roots = sorted(sc - so)              # 现版新增的根域(合并引入, 非新站点)

root_counter = Counter(rd for _,rd in merged)
merged_roots = sorted(root_counter)

print('='*64)
print(f'原版 HEAD~1 (合并前): {len(orig)} 条')
print(f'现版 HEAD   (合并后): {len(cur)}  条')
print('='*64)
print(f'【A】两边都有(不变)        : {len(unchanged)} 条')
print(f'【B】子域并入根域(合并去重): {len(merged)} 条子域 -> {len(merged_roots)} 个根域')
print(f'【C】真删除(脏数据)        : {len(truly_deleted)} 条')
print(f'【D】现版新增根域(合并引入): {len(new_roots)} 条  <- 这些不是新站点, 是被并子域的根域形式')
print('-'*64)
print('校验: A+B+C =', len(unchanged)+len(merged)+len(truly_deleted), '(应=1456)')
print('校验: A+D   =', len(unchanged)+len(new_roots), '(应=1281)')
print('='*64)
print(f'\n【C 真删除的 {len(truly_deleted)} 条脏数据】(拼接错乱 / JSON路径串):')
for d in truly_deleted:
    print('   -', d)
print('\n【B 合并量最大的根域 Top12】(子域越多, 合并掉的条数越多):')
for rd,c in root_counter.most_common(12):
    print(f'   {rd:28s} {c} 个子域 -> 1 个根域 (省 {c-1} 条)')
print('\n【一句话总账】')
print(f'   1456 原版 中, 有 {len(merged)} 条是「同一网站多个子域各算一条」(www./m./api./img./wap.),')
print(f'   整理后每站只留 1 个根域(整站封), 这 {len(merged)} 条被合并去重;')
print(f'   另删 {len(truly_deleted)} 条拼接错乱脏数据;')
print(f'   净条数 = 1456 - {len(merged)} - {len(truly_deleted)} + 因合并新引入的根域 = 1281')
