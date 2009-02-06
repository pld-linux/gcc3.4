#
# TODO:
#   - fix ada build errors
#   - provide as full gcc 3.x as possible without conflicting with gcc 4.x
#   - should be named gcc3.4 or so, gcc3 is too ambiguous
#     (there were 4 different ABIs and very different compatibility issues)
#
# Conditional build:
%bcond_without	cxx
%bcond_with	fortran
%bcond_with	ada		# build without ADA support
%bcond_with	java		# build without Java support
%bcond_with	objc		# build without ObjC support
%bcond_with	ssp		# build with stack-smashing protector support
%bcond_with	multilib	# build with multilib support
%ifnarch amd64 ppc64 s390x sparc64
%undefine	with_multilib
%endif
#
Summary:	GNU Compiler Collection: the C compiler and shared files
Summary(es.UTF-8):	Colección de compiladores GNU: el compilador C y ficheros compartidos
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: kompilator C i pliki współdzielone
Summary(pt_BR.UTF-8):	Coleção dos compiladores GNU: o compilador C e arquivos compartilhados
Name:		gcc3
Version:	3.4.6
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	4a21ac777d4b5617283ce488b808da7b
Source2:	http://www.trl.ibm.com/projects/security/ssp/gcc2_95_3/gcc_stack_protect.m4.gz
# Source2-md5:	07d93ad5fc07ca44cdaba46c658820de
Source3:	%{name}-gcc_visibility.m4
Patch0:		%{name}-info.patch
Patch1:		%{name}-nolocalefiles.patch
Patch2:		%{name}-ada-link-new-libgnat.patch
Patch3:		%{name}-nodebug.patch
Patch4:		%{name}-ssp.patch
Patch5:		%{name}-ada-link.patch
Patch6:		%{name}-pr15666.patch
#
# -fvisibility={default|internal|hidden|protected}
#
# Set the default ELF image symbol visibility to the specified option.
# All symbols will be marked with this unless overrided within the code.
# Using this feature can very substantially improve linking and load times
# of shared object libraries, produce more optimised code, provide near-perfect
# API export and prevent symbol clashes. It is strongly recommended that you
# use this in any shared objects you distribute.
#
# -fvisibility-inlines-hidden
#
# Causes all inlined methods to be marked with __attribute__((visibility("hidden")))
# so that they do not appear in the export table of a DSO and do not require a PLT
# indirection when used within the DSO. Enabling this option can have a dramatic
# effect on load and link times of a DSO as it massively reduces the size
# of the dynamic export table when the library makes heavy use of templates.
# While it can cause bloating through duplication of code within each DSO
# where it is used, often the wastage is less than the considerable space
# occupied by a long symbol name in the export table which is typical when using
# templates and namespaces.
#
# How to Write Shared Libraries: http://people.redhat.com/drepper/dsohowto.pdf
#
Patch7:		%{name}-visibility.patch
Patch8:	%{name}-cxxabi.patch
Patch9:	%{name}-pr-rh.patch
#
Patch20:	%{name}-ada-bootstrap.patch
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.91.0.2
BuildRequires:	bison
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex
%if %{with ada}
BuildRequires:	gcc(ada)
BuildRequires:	gcc-ada
%endif
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel >= 2.2.5-20
BuildRequires:	perl-devel
BuildRequires:	texinfo >= 4.1
BuildRequires:	zlib-devel
Requires:	binutils >= 2:2.15.91.0.2
Requires:	gcc-dirs >= 1.0-3
Provides:	cpp = %{epoch}:%{version}-%{release}
%{?with_ada:Provides:	gcc(ada)}
%{?with_ssp:Provides:	gcc(ssp)}
Conflicts:	glibc-devel < 2.2.5-20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_slibdir	/%{_lib}
%ifarch amd64 ppc64 s390x sparc64
%define		_slibdir32	/lib
%define		_libdir32	/usr/lib
%endif
%ifarch sparc64
%define		rpmcflags	-O2 -mtune=ultrasparc
%endif

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler and some files shared by various
parts of the GNU Compiler Collection. In order to use another GCC
compiler you will need to install the appropriate subpackage.

%description -l es.UTF-8
Un compilador que intenta integrar todas las optimalizaciones y
características necesarias para un entorno de desarrollo eficaz y
estable.

Este paquete contiene el compilador de C y unos ficheros compartidos
por varias partes de la colección de compiladores GNU (GCC). Para usar
otro compilador de GCC será necesario que instale el subpaquete
adecuado.

%description -l pl.UTF-8
Kompilator, posiadający duże możliwości optymalizacyjne niezbędne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera kompilator C i pliki współdzielone przez różne
części kolekcji kompilatorów GNU (GCC). Żeby używać innego kompilatora
z GCC, trzeba zainstalować odpowiedni podpakiet.

%description -l pt_BR.UTF-8
Este pacote adiciona infraestrutura básica e suporte a linguagem C ao
GNU Compiler Collection.

%package libgcc
Summary:	Shared gcc library
Summary(es.UTF-8):	Biblioteca compartida de gcc
Summary(pl.UTF-8):	Biblioteka gcc
Summary(pt_BR.UTF-8):	Biblioteca runtime para o GCC
Group:		Libraries

%description libgcc
Shared gcc library.

%description libgcc -l es.UTF-8
Biblioteca compartida de gcc.

%description libgcc -l pl.UTF-8
Biblioteka dynamiczna gcc.

%description libgcc -l pt_BR.UTF-8
Biblioteca runtime para o GCC.

%package c++
Summary:	C++ support for gcc
Summary(es.UTF-8):	Soporte de C++ para gcc
Summary(pl.UTF-8):	Obsługa C++ dla gcc
Summary(pt_BR.UTF-8):	Suporte C++ para o gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection. It
includes support for most of the current C++ specification, including
templates and exception handling. It does not include a standard C++
library, which is available separately.

%description c++ -l de.UTF-8
Dieses Paket enthält die C++-Unterstützung für den
GNU-Compiler-Collection. Es unterstützt die aktuelle
C++-Spezifikation, inkl. Templates und Ausnahmeverarbeitung. Eine
C++-Standard-Library ist nicht enthalten - sie ist getrennt
erhältlich.

%description c++ -l es.UTF-8
Este paquete añade soporte de C++ al GCC (colección de compiladores
GNU). Ello incluye el soporte para la mayoría de la especificación
actual de C++, incluyendo plantillas y manejo de excepciones. No
incluye la biblioteca estándar de C++, la que es disponible separada.

%description c++ -l fr.UTF-8
Ce package ajoute un support C++ a la collection de compilateurs GNU.
Il comprend un support pour la plupart des spécifications actuelles de
C++, dont les modéles et la gestion des exceptions. Il ne comprend pas
une bibliothéque C++ standard, qui est disponible séparément.

%description c++ -l pl.UTF-8
Ten pakiet dodaje obsługę C++ do kompilatora gcc. Ma wsparcie dla
dużej ilości obecnych specyfikacji C++, nie zawiera natomiast
standardowych bibliotek C++, które są w oddzielnym pakiecie.

%description c++ -l pt_BR.UTF-8
Este pacote adiciona suporte C++ para o gcc.

%description c++ -l tr.UTF-8
Bu paket, GNU C derleyicisine C++ desteği ekler. 'Template'ler ve
aykırı durum işleme gibi çoğu güncel C++ tanımlarına uyar. Standart
C++ kitaplığı bu pakette yer almaz.

%package objc
Summary:	Objective C support for gcc
Summary(de.UTF-8):	Objektive C-Unterstützung für gcc
Summary(es.UTF-8):	Soporte de Objective C para gcc
Summary(fr.UTF-8):	Gestion d'Objective C pour gcc
Summary(pl.UTF-8):	Obsługa obiektowego C dla kompilatora gcc
Summary(tr.UTF-8):	gcc için Objective C desteği
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libobjc = %{epoch}:%{version}-%{release}

%description objc
This package adds Objective C support to the GNU Compiler Collection.
Objective C is a object oriented derivative of the C language, mainly
used on systems running NeXTSTEP. This package does not include the
standard objective C object library.

%description objc -l de.UTF-8
Dieses Paket ergänzt den GNU-Compiler-Collection durch
Objective-C-Support. Objective C ist ein objektorientiertes Derivat
von C, das zur Hauptsache auf Systemen mit NeXTSTEP zum Einsatz kommt.
Die Standard-Objective-C-Objekt-Library ist nicht Teil des Pakets.

%description objc -l es.UTF-8
Este paquete añade soporte de Objective C al GCC (colección de
compiladores GNU). Objective C es un lenguaje orientado a objetos
derivado de C, principalmente usado en sistemas que funcionan bajo
NeXTSTEP. El paquete no incluye la biblioteca de objetos estándar de
Objective C.

%description objc -l fr.UTF-8
Ce package ajoute un support Objective C a la collection de
compilateurs GNU. L'Objective C est un langage orienté objetdérivé du
langage C, principalement utilisé sur les systèmes NeXTSTEP. Ce
package n'inclue pas la bibliothéque Objective C standard.

%description objc -l pl.UTF-8
Ten pakiet dodaje obsługę obiektowego C do kompilatora gcc. Obiektowe
C (objc) jest zorientowaną obiektowo pochodną języka C, używaną
głównie w systemach używających NeXTSTEP. W pakiecie nie ma
standardowej biblioteki objc (która znajduje się w osobnym pakiecie).

%description objc -l tr.UTF-8
Bu paket, GNU C derleyicisine Objective C desteği ekler. Objective C,
C dilinin nesne yönelik bir türevidir ve NeXTSTEP altında çalışan
sistemlerde yaygın olarak kullanılır. Standart Objective C nesne
kitaplığı bu pakette yer almaz.

%package libobjc
Summary:	Objective C Libraries
Summary(es.UTF-8):	Bibliotecas de Objective C
Summary(pl.UTF-8):	Biblioteki Obiektowego C
Group:		Libraries

%description libobjc
Objective C Libraries.

%description libobjc -l es.UTF-8
Bibliotecas de Objective C.

%description libobjc -l pl.UTF-8
Biblioteki Obiektowego C.

%package libobjc-static
Summary:	Static Objective C Libraries
Summary(es.UTF-8):	Bibliotecas estáticas de Objective C
Summary(pl.UTF-8):	Statyczne Biblioteki Obiektowego C
Group:		Development/Libraries
Requires:	%{name}-libobjc = %{epoch}:%{version}-%{release}

%description libobjc-static
Static Objective C Libraries.

%description libobjc-static -l es.UTF-8
Bibliotecas estáticas de Objective C.

%description libobjc-static -l pl.UTF-8
Statyczne biblioteki Obiektowego C.

%package g77
Summary:	Fortran 77 support for gcc
Summary(es.UTF-8):	Soporte de Fortran 77 para gcc
Summary(pl.UTF-8):	Obsługa Fortranu 77 dla gcc
Summary(pt_BR.UTF-8):	Suporte Fortran 77 para o GCC
Group:		Development/Languages/Fortran
Requires:	%{name}-libg2c = %{epoch}:%{version}-%{release}

%description g77
This package adds support for compiling Fortran 77 programs with the
GNU compiler.

%description g77 -l es.UTF-8
Este paquete añade soporte para compilar programas escritos en Fortran
77 con el compilador GNU.

%description g77 -l pl.UTF-8
Ten pakiet dodaje obsługę Fortranu 77 do kompilatora gcc. Jest
potrzebny do kompilowania programów pisanych w języku Fortran 77.

%description g77 -l pt_BR.UTF-8
Suporte Fortran 77 para o GCC.

%package libg2c
Summary:	Fortran 77 Libraries
Summary(es.UTF-8):	Bibliotecas de Fortran 77
Summary(pl.UTF-8):	Biblioteki Fortranu 77
Group:		Libraries

%description libg2c
Fortran 77 Libraries.

%description libg2c -l es.UTF-8
Bibliotecas de Fortran 77.

%description libg2c -l pl.UTF-8
Biblioteki Fortranu 77.

%package libg2c-static
Summary:	Static Fortran 77 Libraries
Summary(es.UTF-8):	Bibliotecas estáticas de Fortran 77
Summary(pl.UTF-8):	Statyczne Biblioteki Fortranu 77
Group:		Development/Libraries
Requires:	%{name}-libg2c = %{epoch}:%{version}-%{release}

%description libg2c-static
Static Fortran 77 Libraries.

%description libg2c -l es.UTF-8
Bibliotecas estáticas de Fortran 77.

%description libg2c-static -l pl.UTF-8
Statyczne biblioteki Fortranu 77.

%package java
Summary:	Java support for gcc
Summary(es.UTF-8):	Soporte de Java para gcc
Summary(pl.UTF-8):	Obsługa Javy dla gcc
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libgcj = %{epoch}:%{version}-%{release}
Requires:	%{name}-libgcj-devel = %{epoch}:%{version}-%{release}
Requires:	java-shared
Provides:	gcj = %{epoch}:%{version}-%{release}

%description java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

%description java -l es.UTF-8
Este paquete añade soporte experimental para compilar programas
Java(tm) y su bytecode en código nativo. Para usarlo también va a
necesitar el paquete libgcj.

%description java -l pl.UTF-8
Wsparcie dla kompilowania programów Java(tm) zarówno do bajt-kodu jak
i do natywnego kodu. Dodatkowo wymagany jest pakiet libgcj, aby można
było przeprowadzić kompilację.

%package java-tools
Summary:	Shared java tools
Summary(es.UTF-8):	Herramientas compartidas de Java
Summary(pl.UTF-8):	Współdzielone narzędzia javy
Group:		Development/Languages/Java
Provides:	jar = %{epoch}:%{version}-%{release}
Provides:	java-shared
Obsoletes:	fastjar
Obsoletes:	jar
Obsoletes:	java-shared

%description java-tools
This package contains tools that are common for every Java(tm)
implementation, such as rmic or jar.

%description java-tools -l es.UTF-8
Este paquete contiene herramientas que son comunes para cada
implementación de Java(tm), como rmic o jar.

%description java-tools -l pl.UTF-8
Pakiet ten zawiera narzędzia wspólne dla każdej implementacji
Javy(tm), takie jak rmic czy jar.

%package libgcj
Summary:	Java Class Libraries
Summary(es.UTF-8):	Bibliotecas de clases de Java
Summary(pl.UTF-8):	Biblioteki Klas Javy
Group:		Libraries
Requires:	zlib

%description libgcj
Java Class Libraries.

%description libgcj -l es.UTF-8
Bibliotecas de clases de Java.

%description libgcj -l pl.UTF-8
Biblioteki Klas Javy.

%package libgcj-devel
Summary:	Development files for Java Class Libraries
Summary(es.UTF-8):	Ficheros de desarrollo para las bibliotecas de clases de Java
Summary(pl.UTF-8):	Pliki nagłówkowe dla Bibliotek Klas Javy
Group:		Development/Libraries
Requires:	%{name}-java = %{epoch}:%{version}-%{release}
Requires:	%{name}-libgcj = %{epoch}:%{version}-%{release}

%description libgcj-devel
Development files for Java Class Libraries.

%description libgcj-devel -l es.UTF-8
Ficheros de desarrollo para las bibliotecas de clases de Java.

%description libgcj-devel -l pl.UTF-8
Pliki nagłówkowe dla Bibliotek Klas Javy.

%package libgcj-static
Summary:	Static Java Class Libraries
Summary(es.UTF-8):	Bibliotecas estáticas de clases de Java
Summary(pl.UTF-8):	Statyczne Biblioteki Klas Javy
Group:		Development/Libraries
Requires:	%{name}-libgcj-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-libstdc++-devel = %{epoch}:%{version}-%{release}

%description libgcj-static
Static Java Class Libraries.

%description libgcj-static -l es.UTF-8
Bibliotecas estáticas de clases de Java.

%description libgcj-static -l pl.UTF-8
Statyczne Biblioteki Klas Javy.

%package libstdc++
Summary:	GNU c++ library
Summary(es.UTF-8):	Biblioteca C++ de GNU
Summary(pl.UTF-8):	Biblioteki GNU C++
Summary(pt_BR.UTF-8):	Biblioteca C++ GNU
Group:		Libraries

%description libstdc++
This is the GNU implementation of the standard C++ libraries, along
with additional GNU tools. This package includes the shared libraries
necessary to run C++ applications.

%description libstdc++ -l de.UTF-8
Dies ist die GNU-Implementierung der Standard-C++-Libraries mit
weiteren GNU-Tools. Dieses Paket enthält die zum Ausführen von
C++-Anwendungen erforderlichen gemeinsam genutzten Libraries.

%description libstdc++ -l es.UTF-8
Este es el soporte de las bibliotecas padrón del C++, junto con
herramientas GNU adicionales. El paquete incluye las bibliotecas
compartidas necesarias para ejecutar aplicaciones C++.

%description libstdc++ -l fr.UTF-8
Ceci est l'implémentation GNU des librairies C++ standard, ainsi que
des outils GNU supplémentaires. Ce package comprend les librairies
partagées nécessaires à l'exécution d'application C++.

%description libstdc++ -l pl.UTF-8
Pakiet ten zawiera biblioteki będące implementacją standardowych
bibliotek C++. Znajdują się w nim biblioteki dynamiczne niezbędne do
uruchomienia aplikacji napisanych w C++.

%description libstdc++ -l pt_BR.UTF-8
Este pacote é uma implementação da biblioteca padrão C++ v3, um
subconjunto do padrão ISO 14882.

%description libstdc++ -l tr.UTF-8
Bu paket, standart C++ kitaplıklarının GNU gerçeklemesidir ve C++
uygulamalarının koşturulması için gerekli kitaplıkları içerir.

%package libstdc++-devel
Summary:	Header files and documentation for C++ development
Summary(de.UTF-8):	Header-Dateien zur Entwicklung mit C++
Summary(es.UTF-8):	Ficheros de cabecera y documentación para desarrollo C++
Summary(fr.UTF-8):	Fichiers d'en-tête et biblitothèques pour développer en C++
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do biblioteki standardowej C++
Summary(pt_BR.UTF-8):	Arquivos de inclusão e bibliotecas para o desenvolvimento em C++
Summary(tr.UTF-8):	C++ ile program geliştirmek için gerekli dosyalar
Group:		Development/Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	%{name}-libstdc++ = %{epoch}:%{version}-%{release}
Requires:	glibc-devel

%description libstdc++-devel
This is the GNU implementation of the standard C++ libraries. This
package includes the header files needed for C++ development and
library documentation.

%description libstdc++-devel -l es.UTF-8
Este es el soporte de las bibliotecas padrón del lenguaje C++. Este
paquete incluye los archivos de inclusión y bibliotecas necesarios
para desarrollo de programas en lenguaje C++.

%description libstdc++-devel -l pl.UTF-8
Pakiet ten zawiera biblioteki będące implementacją standardowych
bibliotek C++. Znajdują się w nim pliki nagłówkowe wykorzystywane przy
programowaniu w języku C++ oraz dokumentacja biblioteki standardowej.

%description libstdc++-devel -l pt_BR.UTF-8
Este pacote inclui os arquivos de inclusão e bibliotecas necessárias
para desenvolvimento de programas C++.

%package libstdc++-static
Summary:	Static C++ standard library
Summary(es.UTF-8):	Biblioteca estándar estática de C++
Summary(pl.UTF-8):	Statyczna biblioteka standardowa C++
Group:		Development/Libraries
Requires:	%{name}-libstdc++-devel = %{epoch}:%{version}-%{release}

%description libstdc++-static
Static C++ standard library.

%description libstdc++-static -l es.UTF-8
Biblioteca estándar estática de C++.

%description libstdc++-static -l pl.UTF-8
Statyczna biblioteka standardowa C++.

%package libffi
Summary:	Foreign Function Interface library
Summary(es.UTF-8):	Biblioteca de interfaz de funciones ajenas
Summary(pl.UTF-8):	Biblioteka zewnętrznych wywołań funkcji
Group:		Libraries

%description libffi
The libffi library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run
time.

%description libffi -l es.UTF-8
La biblioteca libffi provee una interfaz portable de programación de
alto nivel para varias convenciones de llamada. Ello permite que un
programador llame una función cualquiera especificada por una
descripción de interfaz de llamada en el tiempo de ejecución.

%description libffi -l pl.UTF-8
Biblioteka libffi dostarcza przenośnego, wysokopoziomowego
międzymordzia do różnych konwencji wywołań funkcji. Pozwala to
programiście wywoływać dowolne funkcje podając konwencję wywołania w
czasie wykonania.

%package libffi-devel
Summary:	Development files for Foreign Function Interface library
Summary(es.UTF-8):	Ficheros de desarrollo para libffi
Summary(pl.UTF-8):	Pliki nagłówkowe dla libffi
Group:		Development/Libraries
Requires:	%{name}-libffi = %{epoch}:%{version}-%{release}

%description libffi-devel
Development files for Foreign Function Interface library.

%description libffi-devel -l es.UTF-8
Ficheros de desarrollo para libffi.

%description libffi-devel -l pl.UTF-8
Pliki nagłówkowe dla libffi.

%package libffi-static
Summary:	Static Foreign Function Interface library
Summary(es.UTF-8):	Biblioteca libffi estática
Summary(pl.UTF-8):	Statyczna biblioteka libffi
Group:		Development/Libraries
Requires:	%{name}-libffi-devel = %{epoch}:%{version}-%{release}

%description libffi-static
Static Foreign Function Interface library.

%description libffi-static -l es.UTF-8
Biblioteca libffi estática.

%description libffi-static -l pl.UTF-8
Statyczna biblioteka libffi.

%package ada
Summary:	Ada support for gcc
Summary(es.UTF-8):	Soporte de Ada para gcc
Summary(pl.UTF-8):	Obsługa Ady do gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libgnat = %{epoch}:%{version}-%{release}

%description ada
This package adds experimental support for compiling Ada programs.

%description ada -l es.UTF-8
Este paquete añade soporte experimental para compilar programas en
Ada.

%description ada -l pl.UTF-8
Ten pakiet dodaje eksperymentalne wsparcie dla kompilacji programów w
Adzie.

%package libgnat
Summary:	Ada standard libraries
Summary(es.UTF-8):	Bibliotecas estándares de Ada
Summary(pl.UTF-8):	Biblioteki standardowe dla Ady
Group:		Libraries

%description libgnat
This package contains shared libraries needed to run programs written
in Ada.

%description libgnat -l es.UTF-8
Este paquete contiene las bibliotecas compartidas necesarias para
ejecutar programas escritos en Ada.

%description libgnat -l pl.UTF-8
Ten pakiet zawiera biblioteki potrzebne do uruchamiania programów
napisanych w Adzie.

%package libgnat-static
Summary:	Static Ada standard libraries
Summary(pl.UTF-8):	Statyczne biblioteki standardowe dla Ady
Group:		Libraries

%description libgnat-static
This package contains static libraries for programs written in Ada.

%description libgnat-static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne dla programów napisanych w
Adzie.

%prep
%setup -q -n gcc-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%{!?debug:%patch3 -p1}
%{?with_ssp:%patch4 -p1}
%patch5 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p0
%patch9 -p0

%ifarch alpha ia64
# needed for bootstrap using gcc 3.3.x on alpha
# and even using the same 3.4.x(!) (but not Debian's 3.3.x) on ia64
%patch20 -p2
%endif

# because we distribute modified version of gcc...
perl -pi -e 's/(version.*)";/$1 %{?with_ssp:SSP }(PLD Linux)";/' gcc/version.c
perl -pi -e 's@(bug_report_url.*<URL:).*";@$1http://bugs.pld-linux.org/>";@' gcc/version.c

mv ChangeLog ChangeLog.general

%build
# because pr16276 patch modifies configure.ac
cd gcc
%{__autoconf}
cd ..
cp -f /usr/share/automake/config.sub .

rm -rf obj-%{_target_platform} && install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CC="%{__cc}"

%if %{with multilib}
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
CC="$CC" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--program-suffix="3" \
	--enable-version-specific-runtime-libs \
	--enable-shared \
	--enable-threads=posix \
	--enable-__cxa_atexit \
	--enable-languages="c%{?with_cxx:,c++}%{?with_fortran:,f77}%{?with_objc:,objc}%{?with_ada:,ada}%{?with_java:,java}" \
	--enable-c99 \
	--enable-long-long \
%ifnarch ppc
%if %{without multilib}
	--disable-multilib \
%endif
%endif
	--enable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-slibdir=%{_slibdir} \
	--without-x \
	%{_target_platform}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
# - on alpha stage1 needs -O0 for 3.3->3.4 bootstrap (gnat from 3.3 is seriously broken)
# - on ia64 use bootstrap-lean as profiledbootstrap is broken (PR 13882, 15836, 16108)
%{__make} -C obj-%{_target_platform} \
%ifarch ia64
	bootstrap-lean \
%else
	profiledbootstrap \
%endif
	GCJFLAGS="%{rpmcflags}" \
	BOOT_CFLAGS="%{rpmcflags}" \
%ifarch alpha
	STAGE1_CFLAGS="%{rpmcflags} -O0" \
%else
	STAGE1_CFLAGS="%{rpmcflags}" \
%endif
	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}

%if %{with ada}
# cannot build it in parallel
for tgt in gnatlib-shared gnattools gnatlib; do
%{__make} -C obj-%{_target_platform}/gcc $tgt \
	BOOT_CFLAGS="%{rpmcflags}" \
	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_aclocaldir},%{_datadir},%{_infodir}}

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} -j1 install \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	DESTDIR=$RPM_BUILD_ROOT

%ifarch sparc64
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-gcc \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-gcc
%endif

ln -sf gcc3 $RPM_BUILD_ROOT%{_bindir}/cc3
echo ".so gcc3.1" > $RPM_BUILD_ROOT%{_mandir}/man1/cc3.1

%if %{with fortran}
ln -sf g773 $RPM_BUILD_ROOT%{_bindir}/f773
echo ".so g773.1" > $RPM_BUILD_ROOT%{_mandir}/man1/f773.1
%endif

%if %{with ada}
# move ada shared libraries to proper place...
mv -f $RPM_BUILD_ROOT%{_libdir}/gcc/*/*/adalib/*.so.1 \
	$RPM_BUILD_ROOT%{_libdir}
# check if symlink to be made is valid
test -f $RPM_BUILD_ROOT%{_libdir}/libgnat3.so.1
ln -sf libgnat3.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnat3.so
ln -sf libgnarl3.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnarl3.so
ln -sf libgnat3.so $RPM_BUILD_ROOT%{_libdir}/libgnat3.so
ln -sf libgnarl3.so $RPM_BUILD_ROOT%{_libdir}/libgnarl3.so
%endif

cd ..

%if %{with java}
install -d java-doc
cp -f libjava/doc/cni.sgml libjava/READ* java-doc
cp -f fastjar/README java-doc/README.fastjar
cp -f libffi/README java-doc/README.libffi
cp -f libffi/LICENSE java-doc/LICENSE.libffi
%endif

%if %{with objc}
cp -f libobjc/README gcc/objc/README.libobjc
%endif

# include/ contains install-tools/include/* and headers that were fixed up
# by fixincludes, we don't want former
gccdir=$(echo $RPM_BUILD_ROOT%{_libdir}/gcc/*/*/)
mkdir $gccdir/tmp
# we have to save these however
mv -f $gccdir/include/syslimits.h $gccdir/tmp
%{?with_cxx:mv -f $gccdir/include/c++ $gccdir/tmp}
%{?with_fortran:mv -f $gccdir/include/g2c.h $gccdir/tmp}
%{?with_objc:mv -f $gccdir/include/objc $gccdir/tmp}
%{?with_java:mv -f $gccdir/include/{libffi/ffitarget.h,gcj} $gccdir/tmp}
rm -rf $gccdir/include
mv -f $gccdir/tmp $gccdir/include
cp $gccdir/install-tools/include/*.h $gccdir/include
# but we don't want anything more from install-tools
rm -rf $gccdir/install-tools

%if %{with multilib}
ln -sf %{_slibdir}/libgcc_s.so.1 $gccdir/libgcc_s.so
ln -sf %{_slibdir32}/libgcc_s.so.1 $gccdir/libgcc_s_32.so
%endif

%if %{with ssp}
zcat %{SOURCE2} > $RPM_BUILD_ROOT%{_aclocaldir}/gcc_stack_protect.m4
%endif
install %{SOURCE3} $RPM_BUILD_ROOT%{_aclocaldir}/gcc_visibility.m4

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post g77
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun g77
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post java
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun java
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post   -p /sbin/ldconfig libgcc
%postun -p /sbin/ldconfig libgcc
%post   -p /sbin/ldconfig libstdc++
%postun -p /sbin/ldconfig libstdc++
%post   -p /sbin/ldconfig libobjc
%postun -p /sbin/ldconfig libobjc
%post   -p /sbin/ldconfig libg2c
%postun -p /sbin/ldconfig libg2c
%post   -p /sbin/ldconfig libgcj
%postun -p /sbin/ldconfig libgcj
%post   -p /sbin/ldconfig libgnat
%postun -p /sbin/ldconfig libgnat
%post   -p /sbin/ldconfig libffi
%postun -p /sbin/ldconfig libffi

%files
%defattr(644,root,root,755)
%doc ChangeLog.general MAINTAINERS NEWS bugs.html faq.html
%doc gcc/{ChangeLog,ONEWS,README.Portability}
%dir %{_libdir}/gcc/*/*
%dir %{_libdir}/gcc/*/*/include
%{?with_ssp:%{_aclocaldir}/gcc_stack_protect.m4}
%{_aclocaldir}/gcc_visibility.m4

%attr(755,root,root) %{_bindir}/*-gcc*
%attr(755,root,root) %{_bindir}/gcc3
%attr(755,root,root) %{_bindir}/gccbug3
%attr(755,root,root) %{_bindir}/gcov3
%attr(755,root,root) %{_bindir}/cc3
%attr(755,root,root) %{_bindir}/cpp3

%{_mandir}/man1/cc3.1*
%{_mandir}/man1/cpp3.1*
%{_mandir}/man1/gcc3.1*
%{_mandir}/man1/gcov3.1*

%attr(755,root,root) %{_slibdir}/lib*.so
%ifarch ia64
%{_slibdir}/libunwind.a
%endif
%{_libdir}/gcc/*/*/libgcov.a
%{_libdir}/gcc/*/*/libgcc.a
%{_libdir}/gcc/*/*/libgcc_eh.a
%{_libdir}/gcc/*/*/specs
%{_libdir}/gcc/*/*/crt*.o
%if %{with multilib}
%attr(755,root,root) %{_libdir}/gcc/*/*/libgcc_s*.so
%{_libdir}/gcc/*/*/32/libgcc.a
%{_libdir}/gcc/*/*/32/libgcc_eh.a
%{_libdir}/gcc/*/*/32/libgcov.a
%{_libdir}/gcc/*/*/32/crt*.o
%endif
%ifarch ppc
%{_libdir}/gcc/*/*/ecrt*.o
%{_libdir}/gcc/*/*/ncrt*.o
%{_libdir}/gcc/*/*/nof
%dir %{_libdir}/nof
%endif
%attr(755,root,root) %{_libdir}/gcc/*/*/cc1
%attr(755,root,root) %{_libdir}/gcc/*/*/collect2

%{_libdir}/gcc/*/*/include/*.h
%{?with_fortran:%exclude %{_libdir}/gcc/*/*/include/g2c.h}

%files libgcc
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir}*/lib*.so.*
%if %{with multilib}
%attr(755,root,root) %{_slibdir32}/lib*.so.*
%endif

%if %{with cxx}
%files c++
%defattr(644,root,root,755)
%doc gcc/cp/{ChangeLog,NEWS}
%attr(755,root,root) %{_bindir}/g++3
%attr(755,root,root) %{_bindir}/*-g++3
%attr(755,root,root) %{_bindir}/c++3
%attr(755,root,root) %{_bindir}/*-c++3
%attr(755,root,root) %{_libdir}/gcc/*/*/cc1plus
%{_libdir}/gcc/*/*/libsupc++.la
%{_libdir}/gcc/*/*/libsupc++.a
%ifarch ppc
%{_libdir}/gcc/*/*/nof/libsupc++.la
%{_libdir}/gcc/*/*/nof/libsupc++.a
%endif
%if %{with multilib}
%{_libdir32}/gcc/*/*/libsupc++.la
%{_libdir32}/gcc/*/*/libsupc++.a
%endif
%{_mandir}/man1/g++3.1*

%files libstdc++
%defattr(644,root,root,755)
%doc libstdc++-v3/{ChangeLog,README}
%attr(755,root,root) %{_libdir}/gcc/*/*/libstdc++.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/gcc/*/*/libstdc++.so.*.*.*
%endif
%if %{with multilib}
%attr(755,root,root) %{_libdir32}/gcc/*/*/libstdc++.so.*.*.*
%endif

%files libstdc++-devel
%defattr(644,root,root,755)
%doc libstdc++-v3/docs/html
%{_libdir}/gcc/*/*/include/c++
%attr(755,root,root) %{_libdir}/gcc/*/*/libstdc++.so
%{_libdir}/gcc/*/*/libstdc++.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/gcc/*/*/nof/libstdc++.so
%{_libdir}/gcc/*/*/nof/libstdc++.la
%endif
%if %{with multilib}
%attr(755,root,root) %{_libdir32}/gcc/*/*/libstdc++.so
%{_libdir32}/gcc/*/*/libstdc++.la
%endif

%files libstdc++-static
%defattr(644,root,root,755)
%{_libdir}/gcc/*/*/libstdc++.a
%ifarch ppc
%{_libdir}/gcc/*/*/nof/libstdc++.a
%endif
%if %{with multilib}
%{_libdir32}/gcc/*/*/libstdc++.a
%endif
%endif

%if %{with objc}
%files objc
%defattr(644,root,root,755)
%doc gcc/objc/README
%attr(755,root,root) %{_libdir}/gcc/*/*/cc1obj
%attr(755,root,root) %{_libdir}/libobjc.so
%{_libdir}/libobjc.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libobjc.so
%{_libdir}/nof/libobjc.la
%endif
%if %{with multilib}
%attr(755,root,root) %{_libdir32}/libobjc.so
%{_libdir32}/libobjc.la
%endif
%{_libdir}/gcc/*/*/include/objc

%files libobjc
%defattr(644,root,root,755)
%doc libobjc/{ChangeLog,README*}
%attr(755,root,root) %{_libdir}/libobjc.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libobjc.so.*.*.*
%endif
%if %{with multilib}
%attr(755,root,root) %{_libdir32}/libobjc.so.*.*.*
%endif

%files libobjc-static
%defattr(644,root,root,755)
%{_libdir}/libobjc.a
%ifarch ppc
%{_libdir}/nof/libobjc.a
%endif
%if %{with multilib}
%{_libdir32}/libobjc.a
%endif
%endif

%if %{with fortran}
%files g77
%defattr(644,root,root,755)
%doc gcc/f/{BUGS,ChangeLog,NEWS}
%attr(755,root,root) %{_bindir}/g77-*
%attr(755,root,root) %{_bindir}/f77
#%{_infodir}/g77*
%attr(755,root,root) %{_libdir}/gcc/*/*/f771
%{_libdir}/libfrtbegin.a
%{_libdir}/libg2c.la
%attr(755,root,root) %{_libdir}/libg2c.so
%ifarch ppc
%{_libdir}/nof/libfrtbegin.a
%{_libdir}/nof/libg2c.la
%attr(755,root,root) %{_libdir}/nof/libg2c.so
%endif
%if %{with multilib}
%{_libdir32}/libfrtbegin.a
%{_libdir32}/libg2c.la
%attr(755,root,root) %{_libdir32}/libg2c.so
%endif
%{_libdir}/gcc/*/*/include/g2c.h
%{_mandir}/man1/g77.1*
%{_mandir}/man1/f77.1*

%files libg2c
%defattr(644,root,root,755)
%doc libf2c/{ChangeLog,README,TODO}
%attr(755,root,root) %{_libdir}/libg2c.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libg2c.so.*.*.*
%endif
%if %{with multilib}
%attr(755,root,root) %{_libdir32}/libg2c.so.*.*.*
%endif

%files libg2c-static
%defattr(644,root,root,755)
%{_libdir}/libg2c.a
%ifarch ppc
%{_libdir}/nof/libg2c.a
%endif
%if %{with multilib}
%{_libdir32}/libg2c.a
%endif
%endif

%if %{with java}
%files java
%defattr(644,root,root,755)
%doc gcc/java/ChangeLog java-doc/*
%attr(755,root,root) %{_bindir}/gcj*
%attr(755,root,root) %{_bindir}/gij
%attr(755,root,root) %{_bindir}/jcf-dump
%attr(755,root,root) %{_bindir}/jv-*
%attr(755,root,root) %{_bindir}/grepjar
%attr(755,root,root) %{_bindir}/*-gcj*
%attr(755,root,root) %{_libdir}/gcc/*/*/jc1
%attr(755,root,root) %{_libdir}/gcc/*/*/jvgenmain
%{_infodir}/gcj*
%{_mandir}/man1/jcf-*
%{_mandir}/man1/jv-*
%{_mandir}/man1/gij*
%{_mandir}/man1/gcj*
%{_mandir}/man1/grepjar*

%files java-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rmi*
%attr(755,root,root) %{_bindir}/jar
%{_mandir}/man1/rmi*
%{_mandir}/man1/jar*
%{_infodir}/fastjar*

%files libgcj
%defattr(644,root,root,755)
%doc libjava/{ChangeLog,LIBGCJ_LICENSE,NEWS,README,THANKS}
%attr(755,root,root) %{_bindir}/addr2name.awk
%attr(755,root,root) %{_libdir}/lib*cj*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib-org*.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/lib*cj*.so.*
%endif
%{_libdir}/logging.properties

%files libgcj-devel
%defattr(644,root,root,755)
%{_includedir}/java
%{_includedir}/javax
%{_includedir}/gcj
%{_includedir}/j*.h
%{_includedir}/gnu/*
%{_libdir}/gcc/*/*/include/gcj
%dir %{_libdir}/security
%{_libdir}/security/*
%dir %{_datadir}/java
%{_datadir}/java/libgcj*.jar
%{_libdir}/lib*cj.spec
%{_libdir}/lib*cj*.la
%attr(755,root,root) %{_libdir}/lib*cj*.so
%attr(755,root,root) %{_libdir}/lib-org-*.so
%{_libdir}/lib-org-*.la
%ifarch ppc
%{_libdir}/nof/lib*cj*.la
%attr(755,root,root) %{_libdir}/nof/lib*cj*.so
%endif
%{_pkgconfigdir}/libgcj.pc

%files libgcj-static
%defattr(644,root,root,755)
%{_libdir}/lib*cj*.a
%{_libdir}/lib-org-*.a
%ifarch ppc
%{_libdir}/nof/lib*cj*.a
%endif

%files libffi
%defattr(644,root,root,755)
%doc libffi/{ChangeLog,ChangeLog.libgcj,LICENSE,README}
%attr(755,root,root) %{_libdir}/libffi-*.so

%files libffi-devel
%defattr(644,root,root,755)
%{_libdir}/gcc/*/*/include/ffitarget.h
%attr(755,root,root) %{_libdir}/libffi.so
%{_libdir}/libffi.la
%{_includedir}/ffi.h

%files libffi-static
%defattr(644,root,root,755)
%{_libdir}/libffi.a
%endif

%if %{with ada}
%files ada
%defattr(644,root,root,755)
%doc gcc/ada/ChangeLog
%attr(755,root,root) %{_bindir}/gnat*
%attr(755,root,root) %{_bindir}/gpr*
%attr(755,root,root) %{_libdir}/libgnarl*.so
%attr(755,root,root) %{_libdir}/libgnat*.so
%attr(755,root,root) %{_libdir}/gcc/*/*/gnat1
%{_libdir}/gcc/*/*/adainclude
%dir %{_libdir}/gcc/*/*/adalib
%{_libdir}/gcc/*/*/adalib/*.ali
%{_libdir}/gcc/*/*/adalib/g-trasym.o
%{_libdir}/gcc/*/*/adalib/libgccprefix.a
%ifarch %{ix86}
%{_libdir}/gcc/*/*/adalib/libgmem.a
%endif
%{_datadir}/gnat
%{_infodir}/gnat*

%files libgnat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnarl*.so.1
%attr(755,root,root) %{_libdir}/libgnat*.so.1

%files libgnat-static
%defattr(644,root,root,755)
%{_libdir}/gcc/*/*/adalib/libgnarl.a
%{_libdir}/gcc/*/*/adalib/libgnat.a
%endif
