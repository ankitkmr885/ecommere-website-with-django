# echo " BUILD START"
# python3.9 -m pip install -r requirements.txt
# python3.9 manage.py collectstatic --noinput --clear
# echo " BUILD END" 

echo "BUILD START"
python3.9 -m pip install -r requirements.txt
mkdir -p staticfiles_build
python3.9 manage.py collectstatic --noinput --clear --verbosity 0
echo "BUILD END"