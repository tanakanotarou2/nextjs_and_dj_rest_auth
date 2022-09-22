import '../../styles/globals.css';
import type { AppPropsWithLayout } from 'next/app';
import { ThemeProvider } from '@mui/material/styles';
import { Hydrate, QueryClient, QueryClientProvider } from 'react-query';
import React, { useEffect, useState } from 'react';
import { useAtomsDebugValue } from 'jotai/devtools';

import { Provider as JotaiProvider, useAtom } from 'jotai';

import { SnackbarKey, SnackbarProvider } from 'notistack';
import { IconButton, styled } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { defaultTheme } from '@/lib/themes';
import DefaultLayout from '@/components/layouts/DefaultLayout';
import { currentUserAtom } from '@/lib/jotaiAtom';
import { apiClient, refreshToken } from '@/lib/apiClient';


// react-query の設定
const queryClientOptions = {
  defaultOptions: {
    queries: {
      // 5 min
      staleTime: 5 * 60 * 1000,
      // ブラウザのコンポーネントにフォーカスを当てた時に自動でフェッチしない
      refetchOnWindowFocus: false,
    },
  },
};

const DebugAtoms = () => {
  useAtomsDebugValue();
  return null;
};

/*
 * マウント時 認証
 * 参考: https://zenn.dev/catnose99/articles/2169dae14b58b6
 */
function AppInit() {
  // グローバルステートにユーザー情報をセットするためのもの
  const [, setCurrentUser] = useAtom(currentUserAtom);

  useEffect(() => {
    (async function() {
      try {
        await refreshToken();
        // サーバーへのリクエスト（未ログインの場合は401等を返すものとする）
        const user=await apiClient.auth.login_user.$get();
        setCurrentUser(user);
      } catch {
        // 未ログイン（未ログイン時のリダイレクト処理などをここに書いても良いかも）
        setCurrentUser(null);
        localStorage.removeItem('tokenExpireAt');
      }
    })();
  }, []);

  return null;
}


function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  const [queryClient] = useState(() => new QueryClient(queryClientOptions));

  // snackbar の設定
  // ==========================================================
  // xボタンのアクション
  const notistackRef = React.createRef();
  const onClickDismiss = (key: SnackbarKey) => () => {
    // @ts-ignore
    notistackRef.current.closeSnackbar(key);
  };
  // xボタン色を白に
  const ColorIconButton = styled(IconButton)(({ theme }) => ({
    color: '#FFF',
  }));
  const snackbarAction = (key: SnackbarKey) => (
    <ColorIconButton aria-label='close' onClick={onClickDismiss(key)}>
      <CloseIcon />
    </ColorIconButton>
  );

  // layout 設定
  // 各ページのコンポーネントが getLayout 関数を持っている場合はそれを呼び出すようにする。
  // 各ページの実装では getLayout 関数で そのページで使用する Layout を適用する。
  // 参考: https://nextjs.org/docs/basic-features/layouts#with-typescript
  //      https://zenn.dev/hisho/articles/fe9f4ec4a8e691
  // ==========================================================
  // 自動でデフォルトの Layout 設定する場合は後者に適用する
  const getLayout = Component.getLayout ?? ((page) => <DefaultLayout>{page}</DefaultLayout>);
  const layoutComponent = getLayout(<Component {...pageProps} />);

  return (
    <QueryClientProvider client={queryClient}>
      <JotaiProvider>
        <DebugAtoms />
        {/* https://react-query.tanstack.com/guides/ssr#using-nextjs */}
        <Hydrate state={pageProps.dehydratedState}> {/* よくわかっていない. react-query のサンプルに有ったので追加 */}

          <ThemeProvider theme={defaultTheme}>
            <SnackbarProvider
              maxSnack={4}
              // @ts-ignore
              ref={notistackRef}
              action={snackbarAction}
            >
              {layoutComponent}
            </SnackbarProvider>
          </ThemeProvider>
        </Hydrate>
        <AppInit />
      </JotaiProvider>
    </QueryClientProvider>
  );
}

export default MyApp;
