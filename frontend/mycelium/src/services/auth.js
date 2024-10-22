import { createOidcAuth, SignInType } from 'vue-oidc-client/vue3'


const appUrl = `${window.location.origin}/`

const mainOidc = createOidcAuth('mycelium', SignInType.Window, appUrl, {
  authority: process.env.VUE_APP_AUTHENTIK_URL,
  client_id: process.env.VUE_APP_AUTHENTIK_CLIENT_ID,
  response_type: 'code',
  scope: 'openid profile email',
  redirect_uri: `${appUrl}auth/signinwin/mycelium`,
  silent_redirect_uri: `${appUrl}auth/signinsilent/mycelium`,
  post_logout_redirect_uri: appUrl,
})

export default mainOidc
