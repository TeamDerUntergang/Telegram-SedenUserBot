with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sedenbot-environment";
  buildInputs = [
      pkgs.python3
      pkgs.python3.pkgs.setuptools
      pkgs.python3.pkgs.pip
    ];
  shellHook = ''
    export PIP_PREFIX="$(pwd)/_build/pip_packages"
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    export PIP="${pkgs.python3.pkgs.pip.outPath}/bin/pip"
    export PYTHON="${pkgs.python3.outPath}/bin/python"
    unset SOURCE_DATE_EPOCH
    
    $PIP install -r requirements.txt
    
    if [ -f "config.env" ]; then
      $PYTHON seden.py
    fi
    '';
}
