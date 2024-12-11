import { Router } from "express";
import {registerUer, loginUser, logoutUser} from "../controllers/user.controller.js";
import { upload } from "../middlewares/multer.middleware.js";
import {verifyJWT} from "../middlewares/auth.middleware.js";

const router = Router()

router.route("/register").post(
    upload.fields([
        {
            name:"avatar",
            maxCount: 1
        },
        {
            name:"coverImage",
            maxCount: 1
        }
    ]),
    registerUer);

    router.route("/login").post(loginUser)

    //secured routes
    router.route("/logout").post(verifyJWT,  logoutUser)   

export default router