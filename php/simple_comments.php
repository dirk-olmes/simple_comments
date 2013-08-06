<?php
function get_slug()
{
    $slug = htmlspecialchars($_POST['Slug']);
    if (empty($slug))
    {
        die('POST request did not include value for required key "Slug"');
    }
    // make sure that any '/' characters inside the slug does not create directories
    return str_replace('/', '_', $slug);
}

function verify_captcha($captcha_db, $slug)
{
    $challenge = htmlspecialchars($_POST['Challenge']);
    if (empty($challenge))
    {
        die('empty challenge');
    }

    $handle = fopen($captcha_db, 'r');
    $line = fgets($handle);
    while ($line)
    {
        $elements = explode("\t", $line);   // the double quotes are required here ...
        if ($elements[0] == $slug)
        {
            $response = trim($elements[1]);
            if ($challenge != $response)
            {
                die('wrong challenge');
            }
            break;
        }

        $line = fgets($handle);
    }
    fclose($handle);
}

function write_comment($filename, $author, $comment)
{
    $date = date('Y-m-d H:i:s');

    $handle = fopen($filename, 'w');
    fwrite($handle, 'Author: ');
    fwrite($handle, $author);
    fwrite($handle, PHP_EOL);
    fwrite($handle, 'Date: ');
    fwrite($handle, $date);
    fwrite($handle, PHP_EOL);
    fwrite($handle, PHP_EOL);
    fwrite($handle, $comment);
    fwrite($handle, PHP_EOL);
    fclose($handle);
}

function send_email_notification($filename, $recipient)
{
    if (empty($recipient))
    {
        return;
    }

    $subject = 'New blog post comment';
    $message = 'A new comment was posted. It is stored in ' . $filename;

    mail($recipient, $subject, $message);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST')
{
    require 'config.inc.php';

    $slug = get_slug();

    if (isset($verify_captcha) && $verify_captcha)
    {
        verify_captcha($captcha_db, $slug);
    }

    $author = htmlspecialchars($_POST['Author']);
    $comment = htmlspecialchars($_POST['Comment']);

    $dir = $comment_dir . '/' . $slug;
    if (is_dir($dir) == False)
    {
        mkdir($dir, 0755);
    }

    $filename = $dir . '/' . uniqid();
    write_comment($filename, $author, $comment);
    if (isset($recipient))
    {
        send_email_notification($filename, $recipient);
    }
?>

<html>
    <head>
        <title>Your comment was posted</title>
    </head>
    <body>
        <h1>Thank you</h1>
        Your comment was posted and will appear on the blog as soon as a moderator has reviewed it.
    </body>
</html>

<?php
}
?>
