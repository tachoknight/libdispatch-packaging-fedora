#!/bin/bash

MYDIR=$PWD

START_TS=`date`

#BUILD=fedora-rawhide-`uname -i`
BUILD=centos-stream+epel-8-`uname -i`

rm -rf $HOME/rpmbuild
rm -rf $MYDIR/mock-results
mkdir $MYDIR/mock-results
mkdir -p $HOME/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp $PWD/*.patch $HOME/rpmbuild/SOURCES
cp $PWD/libdispatch.spec $HOME/rpmbuild/SPECS

#echo Cleaning $BUILD
mock -r $BUILD --scrub=all

pushd $HOME/rpmbuild/SPECS
echo Now getting the sources...
spectool -g -R ./libdispatch.spec
# Now do the actual build
echo Now gonna hopefully build it
mock --clean -r $BUILD --spec=libdispatch.spec --sources=../SOURCES --resultdir=$MYDIR/mock-results --buildsrpm --rebuild --rpmbuild-opts=--noclean --no-cleanup-after 2>&1 | tee $MYDIR/mock-results/build-output.txt
popd

echo Started:_____$START_TS
echo Ended:_______`date`
