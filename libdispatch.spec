%global toolchain clang
%global reltag 5.3.3-RELEASE


Name:           libdispatch
Version:        5.3.3
Release:        1%{?dist}
Summary:        Apple's Grand Central Dispatch library
License:        ASL 2.0 
URL:            https://github.com/apple/swift-corelibs-libdispatch

Source0:        https://github.com/apple/swift-corelibs-libdispatch/archive/swift-%{reltag}.tar.gz#/corelibs-libdispatch.tar.gz

Patch0:         asprintf.patch

BuildRequires:  clang
BuildRequires:  libbsd-devel
BuildRequires:  ninja-build
BuildRequires:  cmake

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


%package devel
Summary:    Development files for libdispatch
Requires:    %{name}%{?_isa} = %{version}-%{release}


%description devel
Development files for libdispatch


%prep
%setup -q -n swift-corelibs-libdispatch-swift-%{reltag}

%patch0 -p2


%build
%cmake -G Ninja .
%cmake_build


%install
%cmake_install


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
* Sun Jan 31 2021 Ron Olson <tachoknight@gmail.com> 5.3.3-1
- Updated to 5.3.3-RELEASE
* Wed Jan 13 2021 Ron Olson <tachoknight@gmail.com> 5.3.2-1
- First version
