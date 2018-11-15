import { config, shallowMount } from '@vue/test-utils';
import CommentsCollectionComponent from '../../src/components/CommentsCollectionComponent';


const expect = require('chai').expect;

config.methods = {
  fetchCommentsCollectionData() {
      return null;
  }
};

describe('CommentsCollectionComponent', () => {
    const wrapper = shallowMount(CommentsCollectionComponent);

    it('contains textarea element', () => {
        expect(wrapper.contains('#newCommentInput')).to.be.equal(true);
    });

    it('doesnt contain  uploading button with 0 comments', () => {
        expect(wrapper.contains('#uploadButton')).to.be.equal(false);
    });

    it('contains submit post button', () => {
        expect(wrapper.contains('#postCommentBtn')).to.be.equal(true);
    });
});