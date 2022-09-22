import type { AspidaClient, BasicHeaders } from 'aspida'
import type { Methods as Methods0 } from './refresh'

const api = <T>({ baseURL, fetch }: AspidaClient<T>) => {
  const prefix = (baseURL === undefined ? '' : baseURL).replace(/\/$/, '')
  const PATH0 = '/auth/token/refresh'
  const POST = 'POST'

  return {
    refresh: {
      /**
       * アクセストークンをリフレッシュします
       */
      post: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods0['post']['resBody'], BasicHeaders, Methods0['post']['status']>(prefix, PATH0, POST, option).json(),
      /**
       * アクセストークンをリフレッシュします
       */
      $post: (option?: { config?: T | undefined } | undefined) =>
        fetch<Methods0['post']['resBody'], BasicHeaders, Methods0['post']['status']>(prefix, PATH0, POST, option).json().then(r => r.body),
      $path: () => `${prefix}${PATH0}`
    }
  }
}

export type ApiInstance = ReturnType<typeof api>
export default api
