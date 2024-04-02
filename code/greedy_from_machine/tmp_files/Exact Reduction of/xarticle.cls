\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{xarticle}[2017/06/16 v0.1 modified article class]

% Pass class options to the underlying article class
%---------------------------------------------------
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% Load LaTeX's article class
%---------------------------
\LoadClass{article}

% Load required packages
%-----------------------

%\RequirePackage[a4paper, margin=1.2in]{geometry}

\renewcommand*\contentsname{\hfil\small Contents}
\setcounter{tocdepth}{2}

% keywords environment
\newenvironment{keywords}{\centerline{\bf\small
        Keywords}\begin{quote}\centering\small} {\end{quote}}

% abstract environment
\renewenvironment{abstract}{\centerline{\bf\small
        Abstract}\begin{quote}\small}{\tableofcontents\end{quote}}


\let\@skip\baselineskip

\def\contact#1{\hfill \normalfont \IfSubStr{#1}{\string @}{\href{emailto:#1}{#1}}{\href{http://#1}{#1}} \vskip -\@skip}

\def\affiliation#1{\vskip \@skip {\itshape \small #1} \vskip -0.8\@skip}

\renewcommand{\and}{\vskip \@skip \flushleft \normalsize \scshape}
\renewcommand\thefootnote{\@fnsymbol\c@footnote}%
\setcounter{footnote}{1}

\renewcommand\maketitle{%
    %
    \hrule height 2pt \vskip \@skip
    %
    {\flushleft \LARGE \bf \@title}%
    %
    \vskip \@skip%
    %
    {\flushleft \scshape  \@author}%
    %
    \vskip 1.3\@skip%
    %
    \hrule height 0.5pt
    %
    \@thanks
    %
    \vskip 3ex
    %
    \setcounter{footnote}{0}%
    \renewcommand{\thefootnote}{\arabic{footnote}}
    \global\let\maketitle\relax
    \global\let\@thanks\@empty
    \global\let\@author\@empty
    \global\let\@date\@empty
    \global\let\@title\@empty
    \global\let\thanks\relax
    \global\let\title\relax
    \global\let\author\relax
    \global\let\date\relax
    \global\let\and\relax
}

%
%% That's all, folks!
\endinput