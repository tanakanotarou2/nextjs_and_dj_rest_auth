/* eslint-disable */
import type * as Types from '../../@types'

export type Methods = {
  /**
   * Reads and updates UserModel fields
   * Accepts GET, PUT, PATCH methods.
   * 
   * Default accepted fields: username, first_name, last_name
   * Default display fields: pk, username, email, first_name, last_name
   * Read-only fields: pk, email
   * 
   * Returns UserModel fields.
   */
  get: {
    status: 200
    resBody: Types.UserDetail
  }

  /**
   * Reads and updates UserModel fields
   * Accepts GET, PUT, PATCH methods.
   * 
   * Default accepted fields: username, first_name, last_name
   * Default display fields: pk, username, email, first_name, last_name
   * Read-only fields: pk, email
   * 
   * Returns UserModel fields.
   */
  put: {
    status: 200
    resBody: Types.UserDetail
    reqFormat: FormData
    reqBody: Types.UserDetailRequest
  }

  /**
   * Reads and updates UserModel fields
   * Accepts GET, PUT, PATCH methods.
   * 
   * Default accepted fields: username, first_name, last_name
   * Default display fields: pk, username, email, first_name, last_name
   * Read-only fields: pk, email
   * 
   * Returns UserModel fields.
   */
  patch: {
    status: 200
    resBody: Types.UserDetail
    reqFormat: FormData
    reqBody: Types.PatchedUserDetailRequest
  }
}
