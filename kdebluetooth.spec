#
# TODO:
# * make it kdeextragears, not kdebluetooth-only
# * s/Network/"Network/Bluetooth"? 
%define		ver	3.3.2
Summary:	KDE Bluetooth framework
Summary(pl):	Podstawowe ¶rodowisko KDE Bluetooth
Name:		kdebluetooth
Version:	3.3.2
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	kdeextragear-3-%{ver}.tar.bz2
# Source0-md5:	21c83484505cdeec5d3a55b62f0ac451
Patch0:		%{name}_qttylock.cpp_dirtybuild.patch
URL:		http://extragear.kde.org/apps/kdebluetooth/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6.1
BuildRequires:	bluez-libs-devel >= 2.6-2
BuildRequires:	gettext-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel
BuildRequires:	lockdev-devel
BuildRequires:	kdelibs-devel
BuildRequires:	openobex-devel >= 1.0.0
BuildRequires:	qt-devel >= 3.1
BuildRequires:	xrender-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The KDE Bluetooth Framework is a set of tools built on top of Linux'
Bluetooth stack BlueZ. Its goal is to provide easy access to the most
common Bluetooth profiles and to make data exchange with Bluetooth
enabled phones and PDAs as straightforward as possible

%description -l pl
Projekt KDE Bluetooth jest zestawem narzêdzi zbudowanych na górnej
warstiwe stosu Bluetooth BlueZ. Jego celem jest dostarczenie ³atwego
dostêpu do wiêkszo¶ci profili Bluetooth oraz wymiany danych z
telefonami komórkowymi z Bluetooth oraz PDA tak bezpo¶rednio jak to
jest mo¿liwe.

%package devel
Summary:	Header files for kdebluetooth libraries
Summary(pl):	Pliki nag³ówkowe bibliotek kdebluetooth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez-libs-devel
Requires:	kdelibs-devel
# when no baudboy.h interface
Requires:	lockdev-devel

%description devel
Header files for kdebluetooth libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek kdebluetooth.

%prep
%setup -q -n kdeextragear-3-%{ver}
%patch0	-p1

%build
%{__make} -f Makefile.cvs
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--disable-rpath \
	--with-bluetooth-libraries=%{_libdir} \
	--with-qt-libraries=%{_libdir} \
	%{!?with_setup:--with-k3bsetup=no}
cd kdebluetooth
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C kdebluetooth install \
	DESTDIR=$RPM_BUILD_ROOT \
	appsdir=%{_desktopdir}/kde \
	k3bsetup2dir=%{_desktopdir}/kde \
	kde_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT%{_desktopdir}
for www in Application/kbtobexsrv.desktop \
	Settings/{Network/Bluetooth/kcm_kbluetoothd,Peripherals/obex}.desktop \
	System/kbluetoothd.desktop Utilities/*.desktop;
do
	mv -f $RPM_BUILD_ROOT%{_datadir}/applnk/$www $RPM_BUILD_ROOT%{_desktopdir}
done
for www in {kbtobexsrv,{kcm_,}kbluetoothd,obex,dunhandler,kbthandsfree,kbtserialchat,faxhandler,kbtobexclient,kbemusedsrv,kbtobexsrv}.desktop;
do
	echo "Categories=Qt;KDE;Network;" >>$RPM_BUILD_ROOT%{_desktopdir}/$www
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libqobex.so.*.*.*
%attr(755,root,root) %{_libdir}/kde3/kcm_*.so
%{_libdir}/kde3/kcm_*.la
%attr(755,root,root) %{_libdir}/kde3/kio_*.so
%{_libdir}/kde3/kio_*.la
%dir %{_libdir}/kdebluetooth
%attr(755,root,root) %{_libdir}/kdebluetooth/*
%{_iconsdir}/*/*/*/*.png
%{_desktopdir}/*.desktop
%{_datadir}/apps/kbluetoothd
%{_datadir}/apps/kbthandsfree
%{_datadir}/apps/kbtobexclient
%{_datadir}/apps/kdebluetooth
%{_datadir}/apps/konqsidebartng/virtual_folders/services/*.desktop
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/servicetypes/*
%{_datadir}/services/*
%{_datadir}/sounds/*
%{_datadir}/mimelnk/bluetooth
%{_datadir}/config/*
%{_datadir}/desktop-directories/*
%{_datadir}/autostart/kbluetoothd.autostart.desktop

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqobex.so
%{_libdir}/libqobex.la
%{_includedir}/qobex
