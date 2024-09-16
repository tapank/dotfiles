for file in ~/src/* ;
do
	echo "checking $file";
	cd $file;
	git status -s;
	cd ..;
done
