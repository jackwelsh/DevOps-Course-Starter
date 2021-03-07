Vagrant.configure("2") do |config|
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.box = "hashicorp/bionic64"
  config.vm.provision "shell", privileged: false, inline: <<-SHELL

  sudo apt-get update

  # Install pyenv prerequisites
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \ 
    libedit-dev libsqllite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \ 
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

  # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile

  SHELL

  # Reload the shell to pick up pyenv
  config.vm.provision :reload

  # Install python 3.7.7
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyenv install 3.7.7
    pyenv global 3.7.7
    echo 'export PATH="$PYENV_ROOT/3.7.7/python/directory/bin:$PATH"' >> ~/.profile
  
  # Install poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  # Launch app
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    cd /vagrant
    poetry install
    poetry run flask run --host 0.0.0.0
    "}
  end
end
