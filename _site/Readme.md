## Run the website locally 

### Install Rbenv 

First install dependencies 

```
sudo apt update
sudo apt install git curl autoconf bison build-essential \
    libssl-dev libyaml-dev libreadline6-dev zlib1g-dev \
    libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev
```

Install Rbenv 

```
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash
```

Run Rbenv 

```
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

### Install Ruby 

```
rbenv install 2.7.1
rbenv global 2.7.1
```

### Install bunlder

```
gem install bundler
```

### Install Gems 

```
bunlde install 
```

### Run the website

```
bundle exec jekyll serve
```
