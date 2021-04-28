with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sedenbot-environment";
  buildInputs = [
      pkgs.git
      pkgs.nano
      pkgs.python3
      pkgs.python3.pkgs.setuptools
      pkgs.python3.pkgs.pip
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
    
    $PIP install -r requirements.txt
    
    if [ -f "config.env" ]; then
      $PYTHON seden.py
    else
      # first run
      $PYTHON session.py
      mv sample_config.env config.env
      echo "Edit config.env file for your own purpose..."
      sleep 0.5
      nano config.env
      $PYTHON seden.py
    fi
    '';
}
