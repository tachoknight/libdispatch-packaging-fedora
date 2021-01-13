#!/bin/bash

MYDIR=$PWD

START_TS=`date`

rm -rf /home/rolson/rpmbuild
rm $MYDIR/build-output.txt
mkdir -p /home/rolson/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp $PWD/*.conf /home/rolson/rpmbuild/SOURCES
cp $PWD/libdispatch.spec /home/rolson/rpmbuild/SPECS

pushd /home/rolson/rpmbuild/SPECS
spectool -g -R ./libdispatch.spec
# Get the dependencies
dnf builddep -y ./libdispatch.spec
# Now do the actual build
rpmbuild -ba ./libdispatch.spec 2>&1 | tee $MYDIR/build-output.txt
#rpmbuild -bc ./libdispatch.spec 2>&1 | tee $MYDIR/build-output.txt
popd

echo Started:_____$START_TS
echo Ended:_______`date`
