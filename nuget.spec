%include	/usr/lib/rpm/macros.mono
Summary:	Package manager for .NET/Mono development platform
Summary(pl.UTF-8):	Zarządca pakietów dla platformy programistycznej .NET/Mono
Name:		nuget
Version:	2.8.7
Release:	1
License:	Apache v2.0
Group:		Development/Tools
%define	veradd	md510+dhx1
#Source0:	http://download.mono-project.com/sources/nuget/%{name}_%{version}+%{veradd}.orig.tar.bz2
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/%{name}_%{version}+%{veradd}.orig.tar.bz2
# Source0-md5:	0fe8090470bf35f44f705c94d7150037
Source1:	%{name}-core.pc
Source2:	%{name}.sh
Patch0:		%{name}-fix_xdt_hintpath
URL:		http://nuget.org/
BuildRequires:	mono-devel >= 4.0
BuildRequires:	rpmbuild(monoautodeps)
BuildRequires:	sed >= 4.0
Requires:	dotnet-nuget = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} arm aarch64 ia64 mips ppc ppc64 s390x sparc sparcv9 sparc64
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NuGet is the package manager for the Microsoft development platform
including .NET. The NuGet client tools provide the ability to produce
and consume packages. The NuGet Gallery is the central package
repository used by all package authors and consumers.

%description -l pl.UTF-8
NuGet to zarządca pakietów dla platformy programistycznej platformy
Microsoft, w tym .NET. Narzędzia klienckie NuGet pozwalają produkować
i konsumować pakiety. NuGet Gallery to centralne repozytorium pakietów
używane przez wszystkich autorów i konsumentów pakietów.

%package -n dotnet-nuget
Summary:	NuGet package manager library for .NET
Summary(pl.UTF-8):	Biblioteka zarządców pakietów NuGet dla .NET
Group:		Libraries
Requires:	mono >= 4.0

%description -n dotnet-nuget
NuGet package manager library for .NET.

%description -n dotnet-nuget -l pl.UTF-8
Biblioteka zarządców pakietów NuGet dla .NET.

%package -n dotnet-nuget-devel
Summary:	Development files for NuGet .NET library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki .NET NuGet
Group:		Development/Libraries
Requires:	dotnet-nuget = %{version}-%{release}
Obsoletes:	nuget-devel

%description -n dotnet-nuget-devel
Development files for NuGet .NET library.

%description -n dotnet-nuget-devel -l pl.UTF-8
Pliki programistyczne biblioteki .NET NuGet.

%prep
%setup -qn %{name}-git
%{__sed} -i "s/\r//g" src/Core/Core.csproj
%patch0 -p1

# fix compile with Mono4
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
xbuild xdt/XmlTransform/Microsoft.Web.XmlTransform.csproj
xbuild src/Core/Core.csproj /p:Configuration="Mono Release"
xbuild src/CommandLine/CommandLine.csproj /p:Configuration="Mono Release"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_pkgconfigdir},%{_prefix}/lib/mono/nuget}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_pkgconfigdir}/nuget-core.pc
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/nuget

cp -p src/CommandLine/bin/Release/NuGet.Core.dll $RPM_BUILD_ROOT%{_prefix}/lib/mono/nuget
cp -p xdt/XmlTransform/bin/Debug/Microsoft.Web.XmlTransform.dll $RPM_BUILD_ROOT%{_prefix}/lib/mono/nuget
cp -p src/CommandLine/bin/Release/NuGet.exe $RPM_BUILD_ROOT%{_prefix}/lib/mono/nuget

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT.txt CREDITS.txt acknowledgements.md changelog.md
%attr(755,root,root) %{_bindir}/nuget
%{_prefix}/lib/mono/nuget/NuGet.exe

%files -n dotnet-nuget
%defattr(644,root,root,755)
%dir %{_prefix}/lib/mono/nuget
%{_prefix}/lib/mono/nuget/Microsoft.Web.XmlTransform.dll
%{_prefix}/lib/mono/nuget/NuGet.Core.dll

%files -n dotnet-nuget-devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/nuget-core.pc
