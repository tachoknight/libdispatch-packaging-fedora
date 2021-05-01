%global toolchain clang
%global reltag 5.4-RELEASE
%global cmake_version 3.19.3

Name:           libdispatch
Version:        5.4
Release:        1%{?dist}
Summary:        Apple's Grand Central Dispatch library
License:        ASL 2.0 
URL:            https://github.com/apple/swift-corelibs-libdispatch

Source0:        https://github.com/apple/swift-corelibs-libdispatch/archive/swift-%{reltag}.tar.gz#/corelibs-libdispatch.tar.gz
Source1:        https://github.com/Kitware/CMake/releases/download/v%{cmake_version}/cmake-%{cmake_version}.tar.gz

BuildRequires:  clang
BuildRequires:  libbsd-devel
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  chrpath

ExclusiveArch:  x86_64 aarch64 

Provides:       libblocksruntime = %{version}-%{release}
Obsoletes:      libblocksruntime < 7.0.0-5

Epoch:          1

%description
Grand Central Dispatch (GCD or libdispatch) provides 
comprehensive support for concurrent code execution on 
multicore hardware.

libdispatch is currently available on all Darwin platforms. 
This project aims to make a modern version of libdispatch 
available on all other Swift platforms. To do this, we will 
implement as much of the portable subset of the API as 
possible, using the existing open source C implementation.

libdispatch on Darwin is a combination of logic in the xnu 
kernel alongside the user-space Library. The kernel has the 
most information available to balance workload across the 
entire system. As a first step, however, we believe it is 
useful to bring up the basic functionality of the library 
using user-space pthread primitives on Linux. Eventually, a 
Linux kernel module could be developed to support more 
informed thread scheduling.


%package devel
Summary:    Development files for libdispatch
Requires:   %{name}%{?_isa} =  %{epoch}:%{version}-%{release}


%description devel
Development files for libdispatch


%prep
%if 0%{?el8}
# Now we build our own CMake because the one in EPEL8 is too old and
# we can safely build it for all platforms (though will add some time
# to the whole build process)
%setup -q -c -n cmake -a 1
mkdir cmake-build
cd cmake-build
../cmake-%{cmake_version}/bootstrap && make
%endif
%setup -q -n swift-corelibs-libdispatch-swift-%{reltag}


%build
%if 0%{?el8}
# And for CMake, which we built first
export PATH=$PWD/../cmake/cmake-build/bin:$PATH
%endif

%cmake -G Ninja .
%cmake_build


%install
%cmake_install
chrpath --delete %{buildroot}%{_libdir}/libdispatch.so


%files
%license LICENSE
%{_libdir}/libBlocksRuntime.so
%{_libdir}/libdispatch.so
%{_mandir}/man3/*


%files devel
%{_includedir}/Block.h
%{_includedir}/dispatch/*
%{_includedir}/os/*


%changelog
* Sat May 01 2021 Ron Olson <tachoknight@gmail.com> 5.4-1
- Updated to 5.4-RELEASE also added explicit CMake step
  for EPEL8
* Wed Feb 03 2021 Ron Olson <tachoknight@gmail.com> 5.3.3-1
- Initial version based on version 5.3.3-RELEASE
