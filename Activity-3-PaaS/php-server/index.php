<?
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file = '/tmp/sample-app.log';
    $message = file_get_contents('php://input');
    file_put_contents($file, date('Y-m-d H:i:s') . " Received message: " . $message . "\n", FILE_APPEND);
} else {
?>
    <!doctype html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>PHP Application - AWS Elastic Beanstalk</title>
        <meta name="viewport" content="width=device-width">
        <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Lobster+Two" type="text/css">
        <link rel="icon" href="https://awsmedia.s3.amazonaws.com/favicon.ico" type="image/ico">
        <link rel="shortcut icon" href="https://awsmedia.s3.amazonaws.com/favicon.ico" type="image/ico">
        <!--[if IE]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
        <link rel="stylesheet" href="/styles.css" type="text/css">
    </head>

    <body>
        <section class="congratulations">
            <h1>Congratulations!</h1>
            <p>Your AWS Elastic Beanstalk <em>PHP</em> application is now running on your own dedicated environment in the AWS&nbsp;Cloud</p>
            <p>You are running PHP version <?= phpversion() ?></p>

            <?php
            for ($a = 0; $a <= 10; $a++) {
                pow($a, $a);
            }
            ?>

            <p>
                <!-- add mysql connection here -->
                <?php
                $conn = new mysqli($_SERVER['RDS_HOSTNAME'], $_SERVER['RDS_USERNAME'], $_SERVER['RDS_PASSWORD'], 'ebdb');
                // Check connection
                if (mysqli_connect_errno()) {
                    echo "Failed to connect to MySQL: " . mysqli_connect_error();
                    http_response_code(500);
                    exit();
                }
                // clean up table first
                $result = $conn->query("TRUNCATE user");
                for ($a = 0; $a <= 1000; $a++) {
                    $user = "'user" . $a . "'";
                    $result = $conn->query("INSERT into user (id, username) VALUES ($a, $user)");
                }
                mysqli_close($conn);
                echo "Cloud Computing Auto Scaling<br>Engineered for Heavy Load: ";
                echo $a;
                ?>

            </p>


        </section>

        <!--[if lt IE 9]><script src="http://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script><![endif]-->
    </body>

    </html>
<?
}
?>