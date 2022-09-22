import type { NextPageWithLayout } from 'next';
import { Button } from '@mui/material';
import { apiClient, login, logout, refreshToken } from '@/lib/apiClient';
import { useCurrentUser } from '@/components/shared/CurrentUser/hooks/useCurrentUser';
import { useAtom } from 'jotai';
import { currentUserAtom } from '@/lib/jotaiAtom';

const Home: NextPageWithLayout = () => {
  const { currentUser, isAuthChecking } = useCurrentUser();
  const [, setCurrentUser] = useAtom(currentUserAtom);
  const _login = async () => {
    try {
      const res = await login('root', 'spamspam');
      setCurrentUser(res);
    } catch {
      setCurrentUser(null);
    }
  };

  const _logout = async () => {
    try {
      await logout();
      setCurrentUser(null);
    } catch {
    }
  };
  const ping = async () => {
    const res = await apiClient.auth.ping.$get();
    console.log(res);
  };
  const csrf = async () => {
    const res = await apiClient.auth.csrf.$get();
    console.log(res);
  };
  const refresh = async () => {
    const res = await refreshToken();
    console.log(res);
  };
  return (
    <div>
      <div>
        <Button onClick={_login}>login</Button>
        <Button onClick={_logout}>logout</Button>
        <Button onClick={refresh}>refresh</Button>
        <Button onClick={ping}>ping</Button>
        <Button onClick={csrf}>csrf</Button>
      </div>
      <div>
        <p>isAuthChecking: {String(isAuthChecking)}</p>
        <p>currentUser: {JSON.stringify(currentUser)}</p>
      </div>

    </div>
  );
};

export default Home;
