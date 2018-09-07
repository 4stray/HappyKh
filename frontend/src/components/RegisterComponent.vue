<template>
    <div id="panel">
        <ul class="ul_tabs">
            <li><a>Sign in</a></li>
            <li><a class="active" >Sign up</a></li>
        </ul>
        <form id="register" action="">
            <input type="email" placeholder="EMAIL" />
            <input type="password" placeholder="PASSWORD" />
            <input type="password" placeholder="CONFIRM PASSWORD" />
            <button id="btn_sign_up" class="btn_registeration" type="submit" >SIGN UP</button>
        </form>
        <p> OR </p>
        <button id="btn_facebook" class="btn_registeration">Log in with Facebook</button>
    </div>
</template>

<script>
    export default {
        name: "RegisterComponent"
    }
</script>

<style scoped>
    #panel {
        display: flex;
        flex-direction: column;
        background-color: #ffe4c4;
        height: 350px;
        width: 55%;
        margin: 100px auto;
        padding: 40px 20px;
        box-shadow: 5px 5px 10px 0px rgba(0, 0, 0, 0.21);
        border-radius: 10px;
    }
    input {
        width: 100%;
        border: none;
        border-bottom: 1px solid #ff80ab;
        background-color: transparent;
        font-size: 14px;
        outline: none;
        margin: 15px 0;
    }

    .btn_registeration {
        width: 100%;
        color: #fff;
        border: none;
        padding: 10px 25px;
        margin: 5px 0;
        text-transform: uppercase;
        font-weight: 600;
        font-family: "Liberation Sans", sans;
        cursor: pointer;
    }
    #btn_sign_up {
        background-color: #ffc107;
    }
    #btn_facebook {
        background-color: #1565c0;
    }

    #btn_sign_up:hover {
        background-color: #ffccbc;
    }
    #btn_facebook:hover {
        background-color: #40c4ff;
    }

    input:focus {
        border-bottom: 1px solid #b71c1c;
    }

    * {
        margin: 0px auto;
        padding: 0px;
    }
    .ul_tabs {
        width: 100%;
        margin-bottom: 15px;
    }

    .ul_tabs > li {
        position: relative;
        float: left;
        width: 50%;
        list-style: none;
        text-align: center;
    }

    a {
        text-decoration: none;
        text-transform: uppercase;
        font-size: 18px;
        color: #999;
        font-weight: 600;
        padding: 10px;
        display: block;
        border-bottom: 3px solid #999;
    }

    .active{
        color: #ff8383;
        border-bottom: 3px solid #ff8383;
    }


</style>