%define VERSION 3.00
%define RELEASE 1

%define _prefix	/usr/local
%define _bindir %{_prefix}/bin
%define _libdir /usr/lib
%define _ppddir /usr

%define PR1 	ip3600
%define PR2 	ip4600
%define PR3 	mp630
%define PR4 	mp540
%define PR5 	mp240
%define PR6 	mp190
%define PR7 	ip1900
%define BUILD_PR 	%{PR1} %{PR2} %{PR3} %{PR4} %{PR5} %{PR6} %{PR7}

%define PKG1 	ip3600series
%define PKG2 	ip4600series
%define PKG3 	mp630series
%define PKG4 	mp540series
%define PKG5 	mp240series
%define PKG6 	mp190series
%define PKG7 	ip1900series

%define PR1_ID 	333
%define PR2_ID 	334
%define PR3_ID 	336
%define PR4_ID 	338
%define PR5_ID 	341
%define PR6_ID 	342
%define PR7_ID 	346
%define BUILD_PR_ID 	%{PR1_ID} %{PR2_ID} %{PR3_ID} %{PR4_ID} %{PR5_ID} %{PR6_ID} %{PR7_ID}

%define CNBP_LIBS libcnbpcmcm libcnbpcnclapi libcnbpcnclbjcmd libcnbpcnclui libcnbpess libcnbpo

Summary: IJ Printer Driver Ver.%{VERSION} for Linux
Name: cnijfilter-common
Version: %{VERSION}
Release: %{RELEASE}
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Source0: cnijfilter-common-%{version}-%{release}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
Requires:  cups popt
#BuildRequires: gtk-devel cups-devel 

%package -n cnijfilter-%{PKG1}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG2}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG3}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG4}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG5}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG6}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng

%package -n cnijfilter-%{PKG7}
Summary: IJ Printer Driver Ver.%{VERSION} for Linux
License: See the LICENSE*.txt file.
Vendor: CANON INC.
Group: Applications/Publishing
Requires: %{name} >= %{version} cups popt libxml2 gtk2 libtiff libpng


%description
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG1}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG2}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG3}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG4}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG5}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG6}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.

%description -n cnijfilter-%{PKG7}
IJ Printer Driver for Linux. 
This IJ Printer Driver provides printing functions for Canon Inkjet
printers operating under the CUPS (Common UNIX Printing System) environment.


%prep
%setup -q

cd libs
    ./autogen.sh --prefix=%{_prefix} 

cd ../cngpij
    ./autogen.sh --prefix=%{_prefix} --enable-progpath=%{_bindir}

cd ../pstocanonij
    ./autogen.sh --prefix=/usr --enable-progpath=%{_bindir} 

cd ../backend
    ./autogen.sh --prefix=/usr


%build
#make 


%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/cups/filter
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/cups/model

make install DESTDIR=${RPM_BUILD_ROOT}

for PR in %{BUILD_PR}
do
cd  ppd
    ./autogen.sh --prefix=/usr --program-suffix=${PR}
	make clean
	make
	make install DESTDIR=${RPM_BUILD_ROOT}

cd ../cnijfilter
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR} --enable-libpath=%{_libdir}/bjlib --enable-binpath=%{_bindir}
    make clean
    make
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../printui
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR}
    make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../lgmon
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR} --enable-progpath=%{_bindir}
    make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ../cngpijmon
    ./autogen.sh --prefix=%{_prefix} --program-suffix=${PR}
	make clean
    make 
    make install DESTDIR=${RPM_BUILD_ROOT}

cd ..
done

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/bjlib

for PR_ID in %{BUILD_PR_ID}
do
#   install -c -s -m 755 ${PR_ID}/database/*  		${RPM_BUILD_ROOT}%{_libdir}/bjlib
    install -c -m 755 ${PR_ID}/database/*  		${RPM_BUILD_ROOT}%{_libdir}/bjlib
    install -c -s -m 755 ${PR_ID}/libs_bin/*.so.* 	${RPM_BUILD_ROOT}%{_libdir}
done

cd ${RPM_BUILD_ROOT}%{_libdir}
#for PR_ID in %{BUILD_PR_ID}
#do
#	ln -s libcnbpcmcm${PR_ID}.so.* 		libcnbpcmcm${PR_ID}.so
#	ln -s libcnbpcnclapi${PR_ID}.so.*	libcnbpcnclapi${PR_ID}.so
#	ln -s libcnbpcnclbjcmd${PR_ID}.so.* libcnbpcnclbjcmd${PR_ID}.so
#	ln -s libcnbpcnclui${PR_ID}.so.* 	libcnbpcnclui${PR_ID}.so
#	ln -s libcnbpess${PR_ID}.so.* 		libcnbpess${PR_ID}.so
#	ln -s libcnbpo${PR_ID}.so.* 		libcnbpo${PR_ID}.so
#done
cd -


%clean
rm -rf $RPM_BUILD_ROOT


%post
%postun

%post -n cnijfilter-%{PKG1}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG1}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR1_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR1_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR1}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR1}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG2}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG2}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR2_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR2_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR2}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR2}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG3}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG3}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR3_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR3_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR3}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR3}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG4}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG4}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR4_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR4_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR4}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR4}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG5}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG5}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR5_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR5_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR5}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR5}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG6}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG6}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR6_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR6_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR6}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR6}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi

%post -n cnijfilter-%{PKG7}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
%postun -n cnijfilter-%{PKG7}
if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig
fi
# remove cnbp* libs
for LIBS in %{CNBP_LIBS}
do
	if [ -h %{_libdir}/${LIBS}%{PR7_ID}.so ]; then
		rm -f %{_libdir}/${LIBS}%{PR7_ID}.so
	fi	
done
# remove directory
if [ "$1" = 0 ] ; then
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/locale/*/LC_MESSAGES
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/cngpijmon%{PR7}
	rmdir -p --ignore-fail-on-non-empty %{_prefix}/share/printui%{PR7}
	rmdir -p --ignore-fail-on-non-empty %{_libdir}/bjlib
	rmdir -p --ignore-fail-on-non-empty %{_bindir}
fi









%files
%defattr(-,root,root)
%{_libdir}/cups/filter/pstocanonij
%{_libdir}/cups/backend/cnijusb
%{_bindir}/cngpij

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG1}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR1}
%{_bindir}/lgmon%{PR1}
%{_bindir}/printui%{PR1}
%{_ppddir}/share/cups/model/canon%{PR1}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR1}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR1}.mo
%{_prefix}/share/cngpijmon%{PR1}/*
%{_prefix}/share/printui%{PR1}/*

%{_bindir}/cif%{PR1}
%{_libdir}/libcnbp*%{PR1_ID}.so*
%{_libdir}/bjlib/cif%{PR1}.conf
%{_libdir}/bjlib/cnb_%{PR1_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR1_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG2}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR2}
%{_bindir}/lgmon%{PR2}
%{_bindir}/printui%{PR2}
%{_ppddir}/share/cups/model/canon%{PR2}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR2}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR2}.mo
%{_prefix}/share/cngpijmon%{PR2}/*
%{_prefix}/share/printui%{PR2}/*

%{_bindir}/cif%{PR2}
%{_libdir}/libcnbp*%{PR2_ID}.so*
%{_libdir}/bjlib/cif%{PR2}.conf
%{_libdir}/bjlib/cnb_%{PR2_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR2_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG3}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR3}
%{_bindir}/lgmon%{PR3}
%{_bindir}/printui%{PR3}
%{_ppddir}/share/cups/model/canon%{PR3}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR3}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR3}.mo
%{_prefix}/share/cngpijmon%{PR3}/*
%{_prefix}/share/printui%{PR3}/*

%{_bindir}/cif%{PR3}
%{_libdir}/libcnbp*%{PR3_ID}.so*
%{_libdir}/bjlib/cif%{PR3}.conf
%{_libdir}/bjlib/cnb_%{PR3_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR3_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG4}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR4}
%{_bindir}/lgmon%{PR4}
%{_bindir}/printui%{PR4}
%{_ppddir}/share/cups/model/canon%{PR4}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR4}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR4}.mo
%{_prefix}/share/cngpijmon%{PR4}/*
%{_prefix}/share/printui%{PR4}/*

%{_bindir}/cif%{PR4}
%{_libdir}/libcnbp*%{PR4_ID}.so*
%{_libdir}/bjlib/cif%{PR4}.conf
%{_libdir}/bjlib/cnb_%{PR4_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR4_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG5}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR5}
%{_bindir}/lgmon%{PR5}
%{_bindir}/printui%{PR5}
%{_ppddir}/share/cups/model/canon%{PR5}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR5}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR5}.mo
%{_prefix}/share/cngpijmon%{PR5}/*
%{_prefix}/share/printui%{PR5}/*

%{_bindir}/cif%{PR5}
%{_libdir}/libcnbp*%{PR5_ID}.so*
%{_libdir}/bjlib/cif%{PR5}.conf
%{_libdir}/bjlib/cnb_%{PR5_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR5_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG6}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR6}
%{_bindir}/lgmon%{PR6}
%{_bindir}/printui%{PR6}
%{_ppddir}/share/cups/model/canon%{PR6}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR6}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR6}.mo
%{_prefix}/share/cngpijmon%{PR6}/*
%{_prefix}/share/printui%{PR6}/*

%{_bindir}/cif%{PR6}
%{_libdir}/libcnbp*%{PR6_ID}.so*
%{_libdir}/bjlib/cif%{PR6}.conf
%{_libdir}/bjlib/cnb_%{PR6_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR6_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%files -n cnijfilter-%{PKG7}
%defattr(-,root,root)
%{_bindir}/cngpijmon%{PR7}
%{_bindir}/lgmon%{PR7}
%{_bindir}/printui%{PR7}
%{_ppddir}/share/cups/model/canon%{PR7}.ppd
%{_prefix}/share/locale/*/LC_MESSAGES/cngpijmon%{PR7}.mo
%{_prefix}/share/locale/*/LC_MESSAGES/printui%{PR7}.mo
%{_prefix}/share/cngpijmon%{PR7}/*
%{_prefix}/share/printui%{PR7}/*

%{_bindir}/cif%{PR7}
%{_libdir}/libcnbp*%{PR7_ID}.so*
%attr(644, lp, lp) %{_libdir}/bjlib/cif%{PR7}.bscc
%{_libdir}/bjlib/cif%{PR7}.conf
%{_libdir}/bjlib/cnb_%{PR7_ID}0.tbl
%{_libdir}/bjlib/cnbpname%{PR7_ID}.tbl

%doc LICENSE-cnijfilter-%{VERSION}JP.txt
%doc LICENSE-cnijfilter-%{VERSION}EN.txt
%doc LICENSE-cnijfilter-%{VERSION}SC.txt
%doc LICENSE-cnijfilter-%{VERSION}FR.txt


%ChangeLog
