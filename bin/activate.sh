
alias pe="pipenv"

run() {
  pe run app
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
