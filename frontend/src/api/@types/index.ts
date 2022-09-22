/* eslint-disable */
import type { ReadStream } from 'fs'

export type CSRFResponse = {
  csrfToken: string
}

export type LoginRequest = {
  username?: string | undefined
  email?: string | undefined
  password: string
}

/** ログインレスポンス */
export type LoginResponse = {
  user: UserDetail

  /** アクセストークンの有効期限 */
  accessTokenExpiration: string
  /** リフレッシュトークンの有効期限 */
  refreshTokenExpiration: string
}

/** ユーザー情報。ユーザー本人及び上位権限者のみ参照できる情報です */
export type PatchedUserDetailRequest = {
  firstName?: string | undefined
  lastName?: string | undefined
  profileIcon?: (File | ReadStream) | null | undefined
}

export type PingResponse = {
  result: string
}

export type RefreshTokenResponse = {
  /** 新しいトークンの有効期限 */
  accessTokenExpiration: string
}

export type RestAuthDetail = {
  detail: string
}

/** ユーザー情報。ユーザー本人及び上位権限者のみ参照できる情報です */
export type UserDetail = {
  id: number
  /** この項目は必須です。半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。 */
  username: string
  firstName?: string | undefined
  lastName?: string | undefined
  profileIcon?: string | null | undefined
}

/** ユーザー情報。ユーザー本人及び上位権限者のみ参照できる情報です */
export type UserDetailRequest = {
  firstName?: string | undefined
  lastName?: string | undefined
  profileIcon?: (File | ReadStream) | null | undefined
}
