import { Alert, Typography } from '@mui/material';
import { ErrorMessage } from '@hookform/error-message';

/**
 * フィールドの下にエラーメッセージを表示するコンポーネント
 * 項目に対し複数のメッセージがある場合に、このコンポーネントを使用することを想定しています。
 * メッセージが1つの場合は、フィールドの help_text を使用することを検討してください。
 */
interface Props {
  name: string;
  errors: { [x: string]: any; } | undefined;
}

const FieldErrorMessages = ({ name, errors }: Props) => {
  return (
    <ErrorMessage
      errors={errors}
      name={name}
      render={({ messages }) => {
        if (!messages) return false;

        const messageList = Object.entries(messages).map(([type, message]) => (
          <Typography key={type} component='p' variant='caption' sx={{ mt: 0 }}>{message}</Typography>
        ));

        return (<>
          <Alert severity='error' sx={{ mt: 0 }} style={{ marginTop: '8px' }}>
            {messageList}
          </Alert>
        </>);
      }}
    />
  );
};

export default FieldErrorMessages;
