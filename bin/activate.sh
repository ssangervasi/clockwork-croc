
alias pe="pipenv"
export PIPENV_DEV=1

run() {
  pe run python -m clockwork_croc.app
}

disco() {
  pe run python -m disco.cli $@
}

console() {
  pe run ipython
}

refresh() {
  source $BASH_SOURCE;
}
