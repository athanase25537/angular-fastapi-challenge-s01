import { IconDefinition } from "@fortawesome/free-solid-svg-icons";

export class LinkModel {

    constructor(
        public icon: IconDefinition,
        public title: string,
        public path: string
    ) { }
}