# Crawler

This is a crawler for a local public transport API.

Please _ask_ the company _before crawling_ their reverse-engineerable APIs.

## Installation

```bash
wget https://raw.githubusercontent.com/philbu/crawler/main/install.sh
chmod +x install.sh
./install.sh
```

## Post Installation

After the installation, you have to add `base`, `fromStation`, `toStation` and `outputDirectory` to the `config.ini` file.

```ini
[Api]
base = https://.../.../
fromStation = ...
toStation = ...
userAgent = ...

[Directory]
outputDirectory = ...
```

## Cronjob

Add a cronjob (in my case for every 5 minutes)

```
*/5 * * * * /path/to/generated/cronjob.sh
```
