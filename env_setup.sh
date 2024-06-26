read -p "Create new conda env (y/n)? " CONT

if [ "$CONT" == "n" ]; then
  echo "exit";
else
# user chooses to create conda env
# prompt user for conda env name
  echo "Creating new conda environment, choose name: "
  read input_variable
  echo "Name $input_variable was chosen";


  echo "installing base packages"
  conda create --name $input_variable\
  python Django psycopg2-binary beautifulsoup4 requests pandas unidecode
  echo "to exit: source deactivate"
fi