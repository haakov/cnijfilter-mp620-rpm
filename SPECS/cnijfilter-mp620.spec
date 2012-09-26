%define debug_package %{nil}
Name:		cnijfilter-mp620
Version:	3.00
Release:	1%{?dist}
Summary:	Canon drivers for the MP620 printer/scanner with improved PPD files
Group:		Other
License:	Custom
URL:		https://aur.archlinux.org/packages.php?ID=40474

Source:	cnijfilter-mp620-3.00.tar.gz

Patch1:		missing-include.patch
Patch2:		mp610.patch
Patch3:		libpng15.patch
Patch4:		v3.00.patch
Patch5:		ppd.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cups-devel,libtiff-devel,libpng-devel,popt-devel
Requires: cups,libtiff,libpng,popt

%description
A port of the Arch Linux AUR's cnijfilter-mp620 package by mouse256: 
cnijfilter-mp620 3.00-1
https://aur.archlinux.org/packages.php?ID=40474
Canon drivers for the MP620 printer/scanner with improved PPD files

%prep
%setup -q -n %{name}-%{version}


cd cnijfilter-common-3.00
ln -s ../cnijfilter-common-2.80/327 327
%patch1 -p2
%patch2 -p2
%patch3 -p1
%patch4 -p2
cd ../ppdMP620-630en-1.5
%patch5 -p2

%build
cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/libs
./autogen.sh --prefix=/usr ${buildroot}${_libdir} || return 1

cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/cngpij
./autogen.sh --prefix=/usr --enable-progpath=/usr/bin ${buildroot}${_libdir} || return 1

cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/pstocanonij
./autogen.sh --prefix=/usr --enable-progpath=/usr/bin ${buildroot}${_libdir} || return 1

cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/backend
./autogen.sh --prefix=/usr --enable-progpath=/usr/bin ${buildroot}${_libdir} || return 1
	
cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00
make || return 1

cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/cnijfilter
./autogen.sh --prefix=/usr --program-suffix=mp610 ${buildroot}${_libdir} --enable-libpath=/usr/lib/bjlib --enable-binpath=/usr/bin || return 1
make || return 1

%install
cd cnijfilter-common-3.00
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


install -d %{buildroot}/usr/lib/bjlib
install 327/database/*.tbl %{buildroot}/usr/lib/bjlib
install 327/libs_bin/*.so.* %{buildroot}/usr/lib
install -D LICENSE-cnijfilter-3.00EN.txt %{buildroot}/usr/share/licenses/%{name}/license.txt
	
cd %{_builddir}/%{buildsubdir}/cnijfilter-common-3.00/cnijfilter
make install DESTDIR=%{buildroot} || return 1
	
# Now we install the updated PPDs from http://mp610.blogspot.com
cd %{_builddir}/%{buildsubdir}/ppdMP620-630en-1.5
install -d %{buildroot}/usr/share/cups/model
install canonmp620-630en.ppd %{buildroot}/usr/share/cups/model/
install cifmp610.conf %{buildroot}/usr/lib/bjlib/

%clean
rm -rf %{buildroot}
echo "%{buildroot}"

%files
%defattr(-,root,root,-)
%doc
/usr/bin/cifmp610
/usr/bin/cngpij
/usr/lib/bjlib/cifmp610.conf
/usr/lib/bjlib/cnb_3270.tbl
/usr/lib/bjlib/cnbpname327.tbl
/usr/lib/cups/backend/cnijusb
/usr/lib/cups/filter/pstocanonij
/usr/lib/libcnbpcmcm327.so.6.61.1
/usr/lib/libcnbpcnclapi327.so.3.3.0
/usr/lib/libcnbpcnclbjcmd327.so.3.3.0
/usr/lib/libcnbpcnclui327.so.3.3.0
/usr/lib/libcnbpess327.so.3.0.9
/usr/lib/libcnbpo327.so.1.0.3
/usr/share/cups/model/canonmp620-630en.ppd
/usr/share/licenses/cnijfilter-mp620/license.txt

%changelog

