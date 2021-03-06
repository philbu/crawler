#!/bin/bash

set -e

read -p "Enter the default directory of the project [/opt/crawler]: " app_dir
app_dir=${app_dir:-/opt/crawler}

echo "Create directory at \"$app_dir\":"
mkdir "$app_dir" && cd "$app_dir"
echo "Clone git repository:"
git clone https://github.com/philbu/crawler.git "git"
echo "Create virtual environment for python (python3-virtualenv necessary)"
python3 -m virtualenv env && source env/bin/activate && pip install -r git/requirements.txt

echo "Create cronjob script:"
echo "#!/bin/bash" > "$app_dir/cronjob.sh"
echo "cd $app_dir/git" >> "$app_dir/cronjob.sh"
echo "$app_dir/env/bin/python3 -m crawler" >> "$app_dir/cronjob.sh"
chmod +x "$app_dir/cronjob.sh"

echo "Next steps:"
echo "1. Add missing information to git/crawler/config.ini"
echo "2. Create a cronjob with \"crontab -e\" and add"
echo "*/5 * * * * $app_dir/cronjob.sh"
