/* eslint-disable */
import type * as Types from '../../@types'

export type Methods = {
  /**
   * Calls Django logout method and delete the Token object
   * assigned to the current User object.
   * 
   * Accepts/Returns nothing.
   */
  post: {
    status: 200
    resBody: Types.RestAuthDetail
  }
}
