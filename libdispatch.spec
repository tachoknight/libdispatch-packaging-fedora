%global debug_package %{nil}
%global swiftbuild swift-source
%global reltag 5.3.2-RELEASE
%global cmake_version 3.19.3


Name:           libdispatch
Version:        5.3.2
Release:        1%{?dist}
Summary:        Apple's Grand Central Dispatch library
License:        ASL 2.0 
URL:            https://github.com/apple/swift-corelibs-libdispatch

Source0:        https://github.com/apple/swift-corelibs-libdispatch/archive/swift-%{reltag}.tar.gz#/corelibs-libdispatch.tar.gz
%if 0%{?el8}
Source1:        https://github.com/Kitware/CMake/releases/download/v%{cmake_version}/cmake-%{cmake_version}.tar.gz
%endif

BuildRequires:  clang
BuildRequires:  libbsd-devel
BuildRequires:  ninja-build
BuildRequires:  cmake
%if 0%{?el8}
BuildRequires:  make
BuildRequires:  openssl-devel
%endif

Provides:       %{name} = %{version}-%{release}

ExclusiveArch:  x86_64 aarch64 


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
export VERBOSE=1
%if 0%{?el8}
# And for CMake, which we built first if we're on CentOS 8
export PATH=$PWD/../cmake/cmake-build/bin:$PATH
%endif
cmake -G Ninja -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_usr} -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ .
ninja


%install
ninja install


%files
%license LICENSE
%{_includedir}/Block.h
%{_includedir}/dispatch/*
%{_includedir}/os/*
%{_libdir}/libBlocksRuntime.so
%{_libdir}/libdispatch.so
%{_mandir}/man3/*


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* Wed Jan 13 2021 Ron Olson <tachoknight@gmail.com> 5.3.2-1
- First version
