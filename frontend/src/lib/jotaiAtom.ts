import { VariantType } from 'notistack';
import { atomWithReset } from 'jotai/utils';
import { atomWithStorage } from 'jotai/utils';
import { atom } from 'jotai';

/* snackbar message */
export type SnackbarMessageInfo = {
  text: string,
  variant: VariantType,
  autoHideDuration?: number | undefined
}
export const messageAtom = atomWithReset<(string | SnackbarMessageInfo | null)>(null);
messageAtom.debugLabel = 'messages';

export const currentUserAtom = atom<(any | null | undefined)>(undefined);
currentUserAtom.debugLabel = 'currentUser';
