<?php
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

    $slug = htmlspecialchars($_POST['Slug']);
    if (empty($slug))
    {
        die('POST request did not include value for required key "Slug"');
    }
    // make sure that any '/' characters inside the slug does not create directories
    $slug = str_replace('/', '_', $slug);

    $author = htmlspecialchars($_POST['Author']);
    $comment = htmlspecialchars($_POST['Comment']);

    $dir = $comment_dir . '/' . $slug;
    if (is_dir($dir) == False)
    {
        mkdir($dir, 0755);
    }

    $filename = $dir . '/' . uniqid();
    write_comment($filename, $author, $comment);
    send_email_notification($filename, $recipient);
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
