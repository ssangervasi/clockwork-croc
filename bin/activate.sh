
alias pe='pipenv'
alias ped='PIPENV_DEV=1 pe'

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
