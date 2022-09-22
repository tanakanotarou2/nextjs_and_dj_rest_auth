import axios from 'axios';
import aspida from '@aspida/axios';
import api from '../api/$api';
import { addMinutes, compareAsc } from 'date-fns';

const SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'TRACE']; // RFC7231
const appendSlash = (url: string) => {
  if (url && url[url.length - 1] !== '/') return url + '/';
  return url;
};

export const apiClient = api(aspida(axios,
  {
    baseURL: process.env.NEXT_PUBLIC_API_URI,
    withCredentials: true,
    responseType: 'json',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
    },
  }));


/* *********************************** */
/* 認証関連
 *
 * TODO: 別モジュールにしたいのですが、どうすればよいかわからず。
 *       一旦ここで定義します。
 */

/* CSRFトークンの取得 */
const getCsrfToken = async () => {
  const res = await apiClient.auth.csrf.$get();
  return res['csrfToken'];
};

export const login = (username: string, password: string) => {
  return apiClient.auth.login.$post({
    body: {
      username: username,
      password: password,
    },
  }).then(res => {
    const time = (new Date(res.accessTokenExpiration)).getTime();
    localStorage.setItem('tokenExpireAt', String(time));
    return res.user;
  });
};

export const logout = () => {
  localStorage.removeItem('tokenExpireAt');
  return apiClient.auth.logout.$post();
};

/*
 * トークンのリフレッシュ
 * アクセストークンの有効期限が短ければリフレッシュする
 */
export const refreshToken = () => {
  const expiredAt = localStorage.getItem('tokenExpireAt');
  if (!expiredAt) return null;

  const expireAt = new Date(Number(expiredAt));
  const dt = addMinutes(new Date(), 5); // offset. 有効期限切れがこれより短ければリフレッシュする

  if (compareAsc(expireAt, dt) <= 0) {
    localStorage.removeItem('tokenExpireAt');

    return apiClient.auth.token.refresh.$post()
      .then(res => {
        const time = (new Date(res.accessTokenExpiration)).getTime();
        localStorage.setItem('tokenExpireAt', String(time));
      })
      .catch(reason => {
        // console.log('refresh error', reason);
      });
  }
  return null;
};

/* end 認証 */
/* *********************************** */

const EXCLUDE_REFRESH_PATHS = [
  appendSlash(apiClient.auth.token.refresh.$path()),
  appendSlash(apiClient.auth.login.$path()),
  appendSlash(apiClient.auth.csrf.$path()),
];

axios.interceptors.request.use(async (config) => {
  const isAppApiRequest = appendSlash(config.baseURL || '') == appendSlash(process.env.NEXT_PUBLIC_API_URI!);

  if (isAppApiRequest) {
    // 末尾にスラッシュなかったら追加
    config.url = appendSlash(config.url!);

    if (EXCLUDE_REFRESH_PATHS.every(s => !s.endsWith(config.url!))) {
      await refreshToken();
    }
    const headers = Object.assign({}, config['headers']);

    // CSRFトークンの追加
    const isUnsafe = !SAFE_METHODS.includes(config.method?.toUpperCase() || '');
    if (isUnsafe) {
      headers['X-CSRFToken'] = await getCsrfToken();
    }
    config['headers'] = headers;
  }

  return config;
});
