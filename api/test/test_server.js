const chai = require('chai');
const chaiHttp = require('chai-http');
const server = require('./server');
const should = chai.should();

chai.use(chaiHttp);

describe('API', function() {
  it('should list all projects on /projects GET', function(done) {
    chai.request(server)
        .get('/projects')
        .end((err, res) => {
          res.should.have.status(200);
          res.body.should.be.a('object');
          done();
        });
  });
});
