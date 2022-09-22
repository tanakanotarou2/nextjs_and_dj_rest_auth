import {useEffect} from 'react';
import {useAtom} from 'jotai'
import {useResetAtom} from 'jotai/utils'
import {useSnackbar} from "notistack";
import {messageAtom} from "@/lib/jotaiAtom";

const CommonSnackbar = () => {
    /*
     * Snackbar のメッセージ表示を管理する
     * TODO: Snackbar の処理を分離したいのでコンポーネントにしているが、このコンポーネント自体は要素を持たないので、mixinのような形に変更できないですか？
     *
     * document: https://iamhosseindhv.com/notistack/
     */
    const [message] = useAtom(messageAtom);
    const resetMessage = useResetAtom(messageAtom)

    const {enqueueSnackbar} = useSnackbar();

    useEffect(() => {
        if (!!message) {
            resetMessage();
            const option = {autoHideDuration: 5000}
            let txt: string;
            if (typeof message === "string") {
                txt = message
            } else {
                txt = message.text
                // @ts-ignore
                option['variant'] = message.variant
                option['autoHideDuration'] = message.autoHideDuration ?? option["autoHideDuration"]
            }
            if (txt.length > 0) enqueueSnackbar(txt, option)
        }
    }, [message])

    return (<></>)
}

export default CommonSnackbar;
