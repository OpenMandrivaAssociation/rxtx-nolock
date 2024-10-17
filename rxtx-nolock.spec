%define upver	2.2
%define uprel	pre2
%define rel	0.1
#define jni	%{_jnidir}
%define jni	%{_libdir}/%{name}

%define distsuffix edm

Summary:	Parallel and serial communication for the Java Development Toolkit without lockfiles
Name:		rxtx-nolock
Version:	%{upver}
Release:	%mkrel 1
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		https://rxtx.qbang.org/
Source:		http://rxtx.qbang.org/pub/rxtx/rxtx-%{upver}%{uprel}.zip
Patch0:		rxtx22-parche_utsrelease.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	java-devel
BuildRequires:	jpackage-utils
BuildRequires:  libtool automake
BuildRequires:  java-rpmbuild
#BuildRequires:	ant >= 1.7.0
#BuildRequires:	ant-junit >= 1.7.0
#BuildRequires:	junit4
Requires:	java
Requires:	jpackage-utils
ExcludeArch:	ppc ppc64 s390 s390x
Conflicts:      rxtx
Conflicts:      librxtx2.1

%description
rxtx is an full implementation of java commapi which aims to support RS232
IEEE 1284, RS485, I2C and RawIO. This version is compiled with --disable-lockfiles
because normal users does not have the permissions needed to write /var/lock files

%prep
%setup -q -n rxtx-%{upver}%{uprel}
%patch0 -R -p0

#%patch2 -p1 -b .p2
#%patch3 -p1 -b .p3
# remove prebuild binaries

find . -name '*.jar' -exec rm {} \;
find . -name '*.hqx' -exec rm {} \;

%build
export JAVA_HOME=%{java_home}

export CC="%{__cc} ${RPM_OPT_FLAGS/-Werror=format-security/} -I/usr/src/linux-`uname -r`/include/"
export CFLAGS="-I/usr/src/linux-`uname -r`/include/"

./configure --disable-lockfiles
make
iconv -f ISO_8859-1 -t UTF-8 ChangeLog >ChangeLog.utf-8
mv ChangeLog.utf-8 ChangeLog

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_javadir} %{buildroot}%{jni}
make RXTX_PATH=%{buildroot}%{jni} JHOME=%{buildroot}%{_javadir} install
#echo "Driver=gnu.io.RXTXCommDriver" > %{buildroot}%{_javadir}/gnu.io.rxtx.properties
find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL README* TODO
%{_javadir}/*
%{jni}

