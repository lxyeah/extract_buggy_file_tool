import os
import csv
from Git import GitRepository

if __name__ == '__main__':
    pro_name = 'commons-collections'

    local_path = os.path.join('/Users/lixuanye/repos', pro_name)
    remote_path = 'https://github.com/apache/{}.git'.format(pro_name)
    repo = GitRepository(local_path, remote_path)

    commit_list = []
    commit_dics = repo.commits()
    for dic in commit_dics:
        commit_list.append(dic["commit"])

    commit_dic = {}

    true_positive_reports_path = './true_positive_reports/fixed-{}.csv'.format(pro_name)
    with open(true_positive_reports_path, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue
            else:
                buggy_commit = line[6]
                buggy_path = line[7]
                fixer = line[10]
                fixer_path = line[11]

                if buggy_commit not in commit_dic.keys():
                    commit_dic[buggy_commit] = []
                    commit_dic[buggy_commit].append(buggy_path)
                else:
                    if buggy_path not in commit_dic[buggy_commit]:
                        commit_dic[buggy_commit].append(buggy_path)

                if fixer not in commit_dic.keys():
                    commit_dic[fixer] = []
                    commit_dic[fixer].append(fixer_path)
                else:
                    if fixer_path not in commit_dic[fixer]:
                        commit_dic[fixer].append(fixer_path)
                i += 1
    f.close()

    check_dir = pro_name + "_check"
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)

    for commit in commit_list:
        if commit in commit_dic.keys():
            file_paths = commit_dic[commit]
            repo.change_to_commit(commit)
            for file_path in file_paths:
                path = os.path.join(local_path, file_path)
                path_string = file_path.split('.')[0].replace('/', '_')
                java_file = path.split('/')[-1]
                mv = 'mv {} {}'.format(path, './' + check_dir)
                file_name = commit + '-' + path_string + '.txt'
                change_name = 'mv {} {}'.format('./' + check_dir + '/' + java_file, './' + check_dir + '/' + file_name)
                os.system(mv)
                os.system(change_name)

    warning_root_dir = pro_name + "_warnings"
    if not os.path.exists(warning_root_dir):
        os.makedirs(warning_root_dir)

    with open(true_positive_reports_path, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue
            else:
                warning_dir = os.path.join(warning_root_dir, 'warning_' + str(i))
                if not os.path.exists(warning_dir):
                    os.makedirs(warning_dir)

                buggy_commit = line[6]
                buggy_path = line[7]
                fixer = line[10]
                fixer_path = line[11]

                buggy_file = buggy_commit + '-' + buggy_path.split('.')[0].replace('/', '_') + '.txt'
                fixer_file = fixer + '-' + fixer_path.split('.')[0].replace('/', '_') + '.txt'

                mv = 'cp {} {}'.format('./' + check_dir + '/' + buggy_file, './' + warning_dir)
                mv1 = 'cp {} {}'.format('./' + check_dir + '/' + fixer_file, './' + warning_dir)
                os.system(mv)
                os.system(mv1)
                i += 1







