Name:      zint
Version:   2.4.3
Release:   3%{?dist}
Summary:   A barcode generator and library
License:   GPLv3+
URL:       http://www.zint.org.uk
Source:    https://github.com/downloads/zint/zint/%{name}-%{version}.src.tar.gz
Group:     Applications/Engineering
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: cmake
BuildRequires: libpng-devel
BuildRequires: zlib-devel

%description
Zint is a C library for encoding data in several barcode variants. The
bundled command-line utility provides a simple interface to the library.
Features of the library:
- Over 50 symbologies including all ISO/IEC standards, like QR codes.
- Unicode translation for symbologies which support Latin-1 and 
  Kanji character sets.
- Full GS1 support including data verification and automated insertion of 
  FNC1 characters.
- Support for encoding binary data including NULL (ASCII 0) characters.
- Health Industry Barcode (HIBC) encoding capabilities.
- Output in PNG, EPS and SVG formats with user adjustable sizes and colors.
- Verification stage for SBN, ISBN and ISBN-13 data.


%package -n zint-devel
Summary:       Library and header files for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description -n zint-devel 
C library and header files needed to develop applications using %{name}.
The API documentation can be found ont the project website:
http://www.zint.org.uk/zintSite/Manual.aspx



%prep
%setup -q

# remove BSD-licensed file required for Windows only (just to ensure that this package is plain GPLv3+)
rm -f backend/ms_stdint.h

# remove bundled getopt sources (we use the corresponding Fedora package instead)
rm -f frontend/getopt*.*

%build
%cmake CMakeLists.txt
make VERBOSE=1 %{?_smp_mflags}

cat <<EOF >zint-qt.desktop
[Desktop Entry]
Name=Zint Barcode Studio
GenericName=Zint Barcode Studio
Exec=zint-qt
Icon=zint
Terminal=false
Type=Application
Categories=Utility;
EOF


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_datadir}/cmake

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/%{name}
%{_libdir}/libzint.so.*

%files -n %{name}-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}.h
%{_libdir}/libzint.so

%changelog
* Tue Aug 7 2012 Dominique Ribaut - 2.4.2
- update to reflect use of github, see https://github.com/zint/zint for up to date chagelog

* Sat May 22 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.1-2
- Added patch to fix export issue

* Fri May 21 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.1-1
- initial package
