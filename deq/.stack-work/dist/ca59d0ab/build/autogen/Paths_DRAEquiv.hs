{-# LANGUAGE CPP #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
{-# OPTIONS_GHC -fno-warn-implicit-prelude #-}
module Paths_DRAEquiv (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [1,1] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\bin"
libdir     = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\lib\\x86_64-windows-ghc-8.0.2\\DRAEquiv-1.1"
dynlibdir  = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\lib\\x86_64-windows-ghc-8.0.2"
datadir    = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\share\\x86_64-windows-ghc-8.0.2\\DRAEquiv-1.1"
libexecdir = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\libexec"
sysconfdir = "C:\\Users\\mhb_n\\PycharmProjects\\FRABisimV4\\deq\\.stack-work\\install\\82ab0e13\\etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "DRAEquiv_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "DRAEquiv_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "DRAEquiv_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "DRAEquiv_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "DRAEquiv_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "DRAEquiv_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "\\" ++ name)
