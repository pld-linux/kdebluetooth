#
# TODO:
# * applnk->vfolders
# * make it kdeextragears, not kdebluetooth-only 
# * breqs
# * fix files
%define		snap	040410

Summary:	KDE Bluetooth framework
Name:		kdebluetooth
Version:	0.1.%{snap}
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	kdeextragear-3-%{snap}.tar.bz2
URL:		http://k3b.sourceforge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6.1
BuildRequires:	gettext-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel
BuildRequires:	qt-devel >= 3.1
BuildRequires:	xrender-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TODO

%package devel
Summary:	Header files for kdebluetooth library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kdelibs-devel

%description devel
TODO

%prep
%setup -q -n kdeextragear-3

%build
make -f Makefile.cvs
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--disable-rpath \
	--with-qt-libraries=%{_libdir} \
	%{!?with_setup:--with-k3bsetup=no}
cd kdebluetooth	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd kdebluetooth
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	appsdir=%{_desktopdir}/kde \
	k3bsetup2dir=%{_desktopdir}/kde \
	kde_htmldir=%{_kdedocdir}
	

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files 
%defattr(644,root,root,755)
%doc README 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/kdebluetooth/*
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/apps/kdebluetooth
%{_datadir}/applnk/.hidden/*.desktop
%{_datadir}/applnk/*/*/*.desktop
%{_datadir}/applnk/*/*/*/*.desktop
%{_datadir}/applnk/*/*.desktop
%{_datadir}/servicetypes/*
%{_datadir}/services/*
%{_datadir}/sounds/*
%{_iconsdir}/*/*/*/*.png
%{_datadir}/mimelnk/bluetooth/
%{_datadir}/apps/*/*
%{_datadir}/config/*

#TODO - make it vfolders compat.
#%{_desktopdir}/kde/*.desktop

%attr(755,root,root) %{_libdir}/kde3/kcm_*.so
%{_libdir}/kde3/kcm_*.la
%attr(755,root,root) %{_libdir}/kde3/kio_*.so
%{_libdir}/kde3/kio_*.la

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqobex.so
%{_libdir}/libqobex.la
%{_includedir}/qobex/*.h
