#!/bin/bash

MYDIR=$PWD

START_TS=`date`

rm -rf $HOME/rpmbuild
rm $MYDIR/build-output.txt
mkdir -p $HOME/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp $PWD/*.patch $HOME/rpmbuild/SOURCES
cp $PWD/libdispatch.spec $HOME/rpmbuild/SPECS

pushd $HOME/rpmbuild/SPECS
spectool -g -R ./libdispatch.spec
# Get the dependencies
dnf builddep -y ./libdispatch.spec
# Now do the actual build
rpmbuild -ba ./libdispatch.spec 2>&1 | tee $MYDIR/build-output.txt
#rpmbuild -bc ./libdispatch.spec 2>&1 | tee $MYDIR/build-output.txt
popd

echo Started:_____$START_TS
echo Ended:_______`date`
