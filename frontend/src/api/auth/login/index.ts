/* eslint-disable */
import type * as Types from '../../@types'

export type Methods = {
  /**
   * Check the credentials and return the REST Token
   * if the credentials are valid and authenticated.
   * Calls Django Auth login method to register User ID
   * in Django session framework
   * 
   * Accept the following POST parameters: username, password
   * Return the REST Framework Token Object's key.
   */
  post: {
    status: 200
    resBody: Types.LoginResponse
    reqFormat: FormData
    reqBody: Types.LoginRequest
  }
}
