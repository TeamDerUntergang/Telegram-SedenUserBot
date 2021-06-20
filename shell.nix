with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sedenbot-environment";
  buildInputs = with pkgs; [
    git nano python3 chromedriver gnused
    python3.pkgs.setuptools
    python3.pkgs.pip
  ];
  
  shellHook = ''
    export PIP_PREFIX="$(pwd)/_build/pip_packages"
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    # use nix binaries because we don't want to invoke host configs
    export GIT="${pkgs.git.outPath}/bin/git"
    export PIP="${pkgs.python3.pkgs.pip.outPath}/bin/pip"
    export PYTHON="${pkgs.python3.outPath}/bin/python"
    unset SOURCE_DATE_EPOCH

    # update bot
    $GIT pull && $GIT checkout seden
    echo "Fetching dependencies..."
    $PIP install -r requirements.txt
    
    if [ -f "config.env" -a -f "sedenuserbot.session" ]; then
      # update chromedriver path
      sed '/CHROME_DRIVER/d' config.env
      echo "CHROME_DRIVER='${pkgs.chromedriver.outPath}/bin/chromedriver'" >> config.env
      $PYTHON seden.py
    else
      # first run
      $PYTHON session.py
      mv sample_config.env config.env
      echo "Press enter to edit config.env file..." && read >> /dev/null
      nano config.env
      echo "Type 'nix-shell' to start SedenUserBot!"
    fi
    '';
}