import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import { Box, Button, IconButton, Link } from '@mui/material';
import { useRouter } from 'next/router';
import GitHubIcon from '@mui/icons-material/GitHub';
import Head from 'next/head';
import CommonSnackbar from '@/components/shared/CommonSnackbar';
// @ts-ignore
const DefaultLayout = ({ children }) => {
  const router = useRouter();
  const goCreate = () => {
    router.push('/questions/new');
  };
  const goHome = () => {
    router.push('/');
  };
  return (
    <>
      <Head>
        <title>サイトタイトル</title>
        <meta name='description' content='サイトタイトル' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <div style={{ minHeight: '100vh' }}>
        {/* @ts-ignore */}
        <AppBar position='static' sx={{ backgroundColor: 'primary.dark' }}>
          <Toolbar variant='dense'>
            <Link variant='h5' color='inherit' underline='none' component='button' onClick={goHome}>
              サイトタイトル
            </Link>
            <div style={{ flexGrow: 1 }} />
          </Toolbar>
        </AppBar>
        <div style={{ paddingTop: 30, paddingBottom: 20 }}>
          {children}
        </div>
      </div>
      <CommonSnackbar />
    </>
  );
};

export default DefaultLayout;
