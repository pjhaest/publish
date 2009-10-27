% LaTeX document class for manuals, based on fenicsmanual.cls.
%
% Copyright (C) Anders Logg, 2008.
% Licensed under the GNU GPL version 3 or any later version.
%
% Modified by Anna Logg, 2008.

%--- Set up class ----
\ProvidesClass{manual}[2008/12/03 manual]
\NeedsTeXFormat{LaTeX2e}
\LoadClass[12pt,twoside]{book}

%--- Load packages ---
\RequirePackage{graphicx}
\RequirePackage{psfrag}
\RequirePackage{fancyhdr}
\RequirePackage{fancybox}
\RequirePackage{fancyvrb}
\RequirePackage{sectsty}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{makeidx}
\RequirePackage{url}
\RequirePackage[latin1]{inputenc}
\RequirePackage[colorlinks]{hyperref}
\RequirePackage[small]{caption}
%\RequirePackage{here}
%\RequirePackage{stmaryrd}
%\RequirePackage{algorithm}

%--- Misc options ---
\setlength{\parindent}{0pt}
\setlength{\parskip}{12pt}
\allsectionsfont{\sffamily}
\newcommand{\tab}{\hspace*{2em}}
\makeindex

%--- Remove header and footer from blank pages  ---
\let\origdoublepage\cleardoublepage
\newcommand{\clearemptydoublepage}{%
  \clearpage
  {\pagestyle{empty}\origdoublepage}%
}
\let\cleardoublepage\clearemptydoublepage

%--- Print index at end of document ---
\AtEndDocument{\cleardoublepage\printindex}

%--- Variables ---
\newcommand{\@manualtitle}{}
\newcommand{\manualtitle}[1]{\renewcommand{\@manualtitle}{#1}}
\newcommand{\@manualauthor}{}
\newcommand{\manualauthor}[1]{\renewcommand{\@manualauthor}{#1}}
\newcommand{\@manualimage}{\vspace{8cm}}
\newcommand{\manualimage}[1]{\renewcommand{\@manualimage}{
    \begin{center}
      \includegraphics[width=12cm]{#1}
    \end{center}}}
\newcommand{\@manualpackage}{<package unspecified>}
\newcommand{\@manualpackagett}{<package unspecified>}
\newcommand{\manualpackage}[2]{\renewcommand{\@manualpackage}{#1}\renewcommand{\@manualpackagett}{#2}}
\newcommand{\package}{\@manualpackage}
\newcommand{\packagett}{\@manualpackagett}

%--- Commands ---
\renewcommand{\maketitle}{
  \lhead{\textsf{\textbf{\@manualtitle}}}
  \rhead{\textsf{\@manualauthor}}
  \pagestyle{fancy}
  \renewcommand{\footrulewidth}{2pt}
  \renewcommand{\headrulewidth}{2pt}
  \thispagestyle{empty}
  \Large\textsf{\textbf{\@manualtitle}} \\
  \vspace{-0.5cm}
  \hrule height 2pt
  \hfill\large\textsf{\today}
  \vspace{3cm}
  \@manualimage
  \vfill\large\textsf{\textbf{\@manualauthor}} \\
  \hrule height 2pt
  \hfill\large\texttt{www.loggsystems.se}
  \newpage
  \null\vfill
  \normalsize
  %Visit \texttt{http://www.fenics.org/} for the latest version of this manual. \\
  %Send comments and suggestions to \texttt{\@fenicspackagett{}-dev@fenics.org}.
  \pagestyle{empty}
  \cleardoublepage
  \tableofcontents
  \cleardoublepage
  \pagestyle{fancy}}

%--- Environments ---
\DefineVerbatimEnvironment{code}{Verbatim}{frame=single,rulecolor=\color{blue}}
\DefineVerbatimEnvironment{macrocode}{Verbatim}{commandchars=\\\{\},frame=single,rulecolor=\color{blue}}

%--- Macros ---
\newcommand{\dx}{\, \mathrm{d}x}
\newcommand{\dX}{\, \mathrm{d}X}
\newcommand{\ds}{\, \mathrm{d}s}
\newcommand{\dS}{\, \mathrm{d}S}
\newcommand{\R}{\mathbb{R}}
\newcommand{\emp}[1]{\texttt{#1}}
