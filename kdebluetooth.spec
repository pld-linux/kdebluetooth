
%define		_snap	040323

Summary:	TODO
Summary(pl):	TOD0
Name:		kdebluetooth
Version:	0.0.%{_snap}
Release:	0.1
License:	GPL
Group:		X11/Applications/Network
# From kdeextragear-3 kde cvs module
Source0:	http://ep09.pld-linux.org/~adgor/kde/%{name}-%{_snap}.tar.bz2
##%% Source0-md5:	0c186ddb8f3be9ebf5cb1fd5f3a3f411
Patch0:		kde-common-QTDOCDIR.patch
URL:		http://kde-bluetooth.sourceforge.net/
BuildRequires:	automake
BuildRequires:	bluez-sdp-devel
BuildRequires:	kdelibs-devel >= 9:3.2.1
BuildRequires:	openobex-devel
BuildRequires:	xmms-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TODO.

%description -l pl
TODO.

%prep
%setup -q -n %{name}-%{_snap}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs 

%configure \
	--disable-rpath \
	--with-qt-libraries=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} 	

%find_lang %{name}	--with-kde	

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/kde3/*.la
%attr(755,root,root) %{_libdir}/kde3/*.so
%{_datadir}/apps/kdebluetooth
%{_datadir}/services/*
%{_desktopdir}/kde/kdebluetooth.desktop
%{_iconsdir}/[!l]*/*/apps/kdebluetooth.png
